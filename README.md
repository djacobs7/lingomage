# LingoMage

Converting code from one language to another, using LLMs

## Usage

1. Download this repo locally, and install dependencies with `poetry install`
2. Download sample code you would like to translate, for example, code from [this repo](https://github.com/hwchase17/langchain)
3. Setup an openAI key: You can set your API key in code using 'openai.api_key = <API-KEY>', or you can set the environment variable OPENAI_API_KEY=<API-KEY>). If your API key is stored in a file, you can point the openai module at it with 'openai.api_key_path = <PATH>'. You can generate API keys in the OpenAI web interface. See https://onboard.openai.com for details, or email support@openai.com if you have any  questions.
4. Run from the command line: `python3 src/lingomage.py convert data/langchain/tests/unit_tests/prompts/test_prompt.py nodejs .js data/`

## Use cases

### Convert a file between languages
 
`python3 src/lingomage.py convert data/langchain/tests/unit_tests/prompts/test_prompt.py nodejs .js data/`

### Find the external dependencies of a source file

`python3 src/lingomage.py get-dependencies data/langchain/tests/unit_tests/prompts/test_prompt.py` 

Note - currently this doesn't always work, because the LLM doesn't always emit a JSON object.  We need to do some work to fix this.


## TODO:
* Make so it can accuratley convert a single file
* Make it so we consistenyly list dependencies.
* Recursively find and convert dependencies.
* BEtter error handling for files that are too long for the prompt
