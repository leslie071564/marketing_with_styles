import argparse
import os
import openai
import json
from dotenv import load_dotenv
from config import politeness_config, rationality_config 

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION")

generation_settings = {
    "model": "gpt-4o",
    "temperature": 1,  # adjust temperature for different randomness in response.
    "max_tokens": 1024, # adjust this if the output is cropped.
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "response_format": {
        "type": "json_object"
    },
}

def generate_task_description(style_1, style_2, allow_content_change=True):
    task_descr = [
        "Different people may prefer different types of expression in an advertisement.",
        "Consequently, even for the same content of an advertisement, how it is conveyed may affect the effectiveness of the advertisement.",
        "The following is a tourism advertisement article.",
        f"Without changing the content and the order of the text, please rewrite the article line by line in Japanese with {style_1} and {style_2} style of speaking, respectively."
        ]

    if not allow_content_change:
        task_descr.append("You must not omit or remove any contents in the given text.")

    # for json output format.
    task_descr.append('\nProvide the re-written article in json format.') 

    return ' '.join(task_descr)


def rewrite(config, sentences):
    task_descr = generate_task_description(style_1=config['keywords'][0], # ex: 'polite/formal (フォーマル)'
                                           style_2=config['keywords'][1], # ex: 'casual (カジュアル)' 
                                           allow_content_change=config['allow_content_change'])

    few_shot_samples = config['few_shots']

    # prompt ex: "1. はじめまして、観光施設の案内役を務めるライカと申します。 \n2. 今日は、京都に位置し、重要文化財にも指定されている旧三井家下鴨別邸をご紹介いたします。この施設は旧三井家の洗練された美意識が随所に反映されています。 \n3. この旧三井家下鴨別邸は、下鴨神社の南側に位置し、かつての豪商である旧三井家の別邸として知られています。"
    prompt = ' \n'.join(f'{i}. {sent}' for i, sent in enumerate(sentences, 1)) 

    response = openai.chat.completions.create(
        **generation_settings,
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": task_descr # provide task description.
                }
            ]
            },
            *few_shot_samples, # provide few-shot example(s).
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt # sentences to be re-wrote (as enumerated list.)
                }
            ]
            },
        ],
    )

    # parse response.
    res_text = response.choices[0].message.content
    #print(res_text)
    res_json = json.loads(res_text)

    # quality check.
    for key in config['output_keys']:
        if key not in res_json:
            raise KeyError(f"Key '{key}' not found in open-ai response.")
        if len(res_json[key]) != len(sentences):
            raise ValueError(f"The output for '{key}' must be exactly {len(sentences)} long.")
    return res_json
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fn', default='./data/shimogamo.txt')
    parser.add_argument('--output_fn', default='./data/shimogamo_4_styles.json')
    args = parser.parse_args()

    # extract PR text from file.
    sentences_raw = [sent.strip() for sent in open(args.input_fn, 'r')]

    results = {'Raw': sentences_raw}
    # step-1: rationality rewrite. 
    res = rewrite(rationality_config, sentences_raw)
    for key1 in res: # 'Rational Style' and 'Emotional Style'.
        results.update({key1.split(' ')[0]: res[key1]})
        
        # step-2: politeness rewrite.
        res_politeness = rewrite(politeness_config, res[key1])
        for key2 in res_politeness: # 'Formal Style' and 'Casual Style':
            results.update({f"{key1.split(' ')[0]}_{key2.split(' ')[0]}": res_politeness[key2]})

    # save result to file.
    with open(args.output_fn, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)