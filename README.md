# 🧙‍♂️ LingoMage

Converting code from one language to another, using LLMs


## What's the goal of this project?

We want to make it so you can feed in an opensource project in any language, and output a working version of that opensource project in a different language.  Think of converting langchain into javascript; converting pandas into C#, or converting the tidyverse into python.

## Usage

1. Download this repo locally, and install dependencies with `poetry install`
2. Download sample code you would like to translate, for example, code from [this repo](https://github.com/hwchase17/langchain)
3. Setup an openAI key: You can set your API key in code using 'openai.api_key = <API-KEY>', or you can set the environment variable `OPENAI_API_KEY=<API-KEY>`. If your API key is stored in a file, you can point the openai module at it with 'openai.api_key_path = <PATH>'. You can generate API keys in the OpenAI web interface. See https://onboard.openai.com for details, or email support@openai.com if you have any  questions.
4. Run `poetry shell` to entry poetry virtualenv
5. Run from the command line: `python3 src/lingomage.py convert {your_file_path_here} {output_language} {output_file_extension} {where_to_save_output}`

## Use cases

### Convert a file between languages
 
`python3 src/lingomage.py convert data/langchain/tests/unit_tests/prompts/test_prompt.py nodejs .js data/`

### Find the external dependencies of a source file

`python3 src/lingomage.py get-dependencies {optional_your_file_here}` 

Note - currently this doesn't always work, because the LLM doesn't always emit a JSON object.  We need to do some work to fix this.


## TODOS
* Make so it can accurately convert a single file
* Make it so we consistently list dependencies.
* Recursively find and convert dependencies.
* Better error handling for files that are too long for the prompt
* Try starting from the tests files and working out way inwards

## CONTRIBUTING

Heck yeah, join in.  If you are reading this, you can contribute!