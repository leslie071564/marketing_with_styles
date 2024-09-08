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

## Generate Questionnaire for preferred style elicitation
TBA
