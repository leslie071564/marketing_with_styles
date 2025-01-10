## Setup
1. Install packages listed in requirements.

2. Create a config file named `.env` which contains the following line:
    ```sh
    OPENAI_API_KEY=...
    OPENAI_ORGANIZATION=...
    ```

## Generate PR text with four different styles
Run the following python code:
```sh
python rewrite_with_gpt.py --input_fn ./data/shimogamo.txt --output_fn ./data/shimogamo.json
```
The results will be saved to `./data/shimogamo.json`.

The default language is Japanese, but we also support generation in other languages such as English and Traditional Chinese. Prepare the input file in the target language and use the following command:
```sh
python rewrite_with_gpt.py --input_fn ./data/shimogamo_en.txt --output_fn $OUTPUT_FILE --language English
```
```sh
python rewrite_with_gpt.py --input_fn ./data/shimogamo_ch.txt --output_fn $OUTPUT_FILE --language "Traditional Chinese"
```

## Generate Questionnaire for preferred style elicitation
TBA
