import os
import json
import argparse
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.organization = os.environ.get("OPENAI_ORGANIZATION")

STYLE_PR_FUNCTION = [
  {
      "type": "function",
      "function": {
          "name": "get_four_styles",
          "parameters": {
              "type": "object",
              "properties": {
                  "rational and formal": {"type": "string"},
                  "rational and causal": {"type": "string"},
                  "emotional and formal": {"type": "string"},
                  "emotional and causal": {"type": "string"},
              },
          },
          "required": ["rational and formal", "rational and causal", "emotional and formal", "emotional and causal"],
      },
  }
]

def pr_with_styles(pr_target, language='Japanese'): 
    questionnaire_instruction = f"""Different people may prefer different types of expression in an advertisement. Consequently, even for the same content of an advertisement, how it is conveyed may affect the effectiveness of the advertisement. For instance:
    - A more rational way of speaking v.s a more emotional way of speaking
    - A more polite/formal way of speaking v.s. a more casual way of speaking

    Giving the following product/service/topic, please generate a one-line advertisement article in {language} with each style of speaking, respectively:
    - rational and polite/formal (理性的かつフォーマル)
    - rational and casual (理性的かつカジュアル)
    - emotional and polite/formal (感性的かつフォーマル)
    - emotional and casual (感性的かつカジュアル)
    Do as much as you can to make advertisements of all styles equally attractive.

    [Target of advertisement] {pr_target}"""
    #print(questionnaire_instruction)

    response = openai.chat.completions.create(
        #**generation_settings,
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": questionnaire_instruction
                }
            ]
            },
        ],
        tools=STYLE_PR_FUNCTION,
    )
    res = response.choices[0].message.tool_calls[0].function.arguments
    pr_texts = json.loads(res) 
    #print(pr_texts)
    return pr_texts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr_targets', nargs='+', required=True)
    parser.add_argument('-l', '--language', default='Japanese')
    parser.add_argument('-o', '--output_fn', default='./data/questionnaire.json')
    args = parser.parse_args()

    results = []
    for target in args.pr_targets:
        pr_texts = pr_with_styles(target, args.language)
        results.append({
            'pr_target': target,
            'pr_texts': pr_texts
        })
    #print(results)

    # save to file.
    with open(args.output_fn, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)