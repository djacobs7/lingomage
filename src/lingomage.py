from pathlib import Path
import openai
import json
import typer

app = typer.Typer()


def get_src(path):
    f= open(path, "r")
    src = f.read()
    return src

def parse_result(result):
    return result['choices'][0]['message']['content']

def last_message(messages):
    return messages[-1]['content']


def cc(messages):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    messages.append( {"role": "assistant", "content": parse_result(result)})
    return messages

@app.command()
def convert( src_path = typer.Argument("data/langchain/tests/unit_tests/prompts/test_prompt.py", help="Path to the source code file you want to convert"), 
            output_language = typer.Argument("nodejs",help="The language you want to convert the code into"), 
            output_suffix = typer.Argument(".js", help="Suffix for output files"),
            project_root = typer.Argument("data/", help = "parent directory of the project containnig the source file. ( e.g if the source file is data/langchain/a/b/c.py, then project_root should be 'data/')")
            ):
    """
    Convert a source code file into the languag eof your choice. Outputs a new source code file to your file system.
    """
    src_path = Path(src_path)
    src = get_src(src_path)

    messages = cc([
        {"role": "system", "content": "You are a software developer assistant."},
        {"role": "user", "content": f"Convert the methods in the code below to {output_language}.  Make sure to convert the entire file. Do not write code for any external requirements. If something is not easy to convert, do your best.  SOURCE: {src}. "}
    ])

    blurb = last_message(messages)
    messages.append({"role": "user", "content":"Please double check your work.  Make sure that you do not write code for any external libraries.  Do not add placeholder code for external libraries. Also return the ENTIRE revised code."})
    messages = cc(messages)

    messages.append({"role": "user", "content":"Can you double check your work and make sure that you ported all of the code and not just a segment? Please put the entire code below:"})
    messages = cc(messages)

    blurb2 = last_message(messages)
    code = blurb2.split("```")[1]

    output_root = Path("out")
    output_path = output_root.joinpath( src_path.relative_to(project_root).with_suffix(output_suffix) )
    output_path.parent.mkdir(parents = True, exist_ok=True)
    with open(output_path,"w") as f:
        f.write(code)

@app.command()
def get_dependencies( src_path = typer.Argument("data/langchain/tests/unit_tests/prompts/test_prompt.py", help="Path to the source code file you want to analyze")):
    """
    Return a list of dependencies for a source code file.
    """
    src_path = Path(src_path)
    src = get_src(src_path)
    messages = cc([
        {"role": "system", "content": "You are a software developer assistant."},
        {"role": "user", "content": f"""Identify any require or import statements for the following source code.  
         Return a list of file paths where you think those files are on the file system. 
         
         The output should be formatted like this:
         [
            {{"code": "import pytest", "path": "<project_root>/venv/lib/python<version>/site-packages/pytest"}},
            {{"code": "from langchain.prompts.prompt import PromptTemplate", "path": "xcompile/data/langchain/prompts/prompt.py"}},
         ]

         The the source code is stored at: {src_path}
         SOURCE: {src}. 
         """
         }
    ])

    blurb = last_message(messages)
    return json.loads(blurb)


# root_data_dir =Path("xcompile/data/")
# src_path = Path(root_data_dir).joinpath("langchain/tests/unit_tests/prompts/test_prompt.py")

# src_path = Path(root_data_dir).joinpath("langchain/langchain/prompts/prompt.py")
# result = get_dependencies(src_path)
# print(result)

# convert( src_path, "nodejs", ".js" )




if __name__ == "__main__":
    app()