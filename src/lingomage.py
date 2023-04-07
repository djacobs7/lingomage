from pathlib import Path
import openai
import json
import typer
from rich import print
from models import Dependency, DependencyTree, MagePath

app = typer.Typer()


def get_src(path):
    f = open(path, "r")
    src = f.read()
    return src


def parse_result(result):
    return result["choices"][0]["message"]["content"]


def last_message(messages):
    return messages[-1]["content"]


def chat_completion(messages):
    print("Sending query to OpenAI...")
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=messages,
    )
    messages.append({"role": "assistant", "content": parse_result(result)})

    return messages


@app.command()
def convert(
    src_path=typer.Argument(
        "examples/fizzbuzz.py",
        help="Path to the source code file you want to convert",
    ),
    output_language=typer.Argument(
        "javascript", help="The language you want to convert the code into"
    ),
    output_suffix=typer.Argument(".js", help="Suffix for output files"),
    project_root=typer.Argument(
        ".",
        help="parent directory of the project containing the source file. ( e.g if the source file is data/directory/a/b/c.py, then project_root should be 'data/')",
    ),
):
    """
    Convert a source code file into the languag eof your choice. Outputs a new source code file to your file system.
    """
    src_path = Path(src_path)
    src = get_src(src_path)

    messages = chat_completion(
        [
            {"role": "system", "content": "You are an expert software developer assistant."},
            {
                "role": "user",
                "content": f"Convert the methods in the code below to {output_language}.  Make sure to convert the entire file. Do not write code for any external requirements. If something is not easy to convert, do your best.  SOURCE: {src}. ",
            },
        ]
    )
    messages.append(
        {
            "role": "user",
            "content": "Please double check your work.  Make sure that you do not write code for any external libraries.  Do not add placeholder code for external libraries. Also return the ENTIRE revised code.",
        }
    )
    messages = chat_completion(messages)

    messages.append(
        {
            "role": "user",
            "content": "Can you double check your work and make sure that you ported all of the code and not just a segment? Please put the entire code below:",
        }
    )
    messages = chat_completion(messages)

    messages = last_message(messages)
    code = messages.split("```")[1]

    output_root = Path("out")
    output_path = output_root.joinpath(
        src_path.relative_to(project_root).with_suffix(output_suffix)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(code)
    print(f"Writing output to {output_path}")


@app.command()
def get_dependencies(
    src_path=typer.Argument(
        "examples/json_loader.py",
        help="Path to the source code file you want to analyze",
    )
):
    """
    Return a list of dependencies for a source code file. Pipe the output to a file if you want to save.
    """
    src_path = Path(src_path)
    src = get_src(src_path)
    messages = chat_completion(
        [
            {"role": "system", "content": "You are a software developer assistant."},
            {
                "role": "user",
                "content": f"""Identify any require or import statements for the following source code.  
         Return a list of file paths where you think those files are on the file system. 
         
         The output should be formatted like this:
         [
            {{"code": "import pytest", "path": "<project_root>/venv/lib/python<version>/site-packages/pytest", "type": "package"}},
            {{"code": "from string import Formatter", "path": "<project_root>/lib/string.py", "type": "python_native"}},
            {{"code": "from langchain.prompts.prompt import PromptTemplate", "path": "xcompile/data/langchain/langchain/prompts/prompt.py", "type":"file"}},


         ]

         If given source code doesn't have any require or import statements, simply return '[]'.  Only return JSON.

         The the source code is stored at: {src_path}
         SOURCE: {src}. 

         OUTPUT:
         
         """,
            },
        ]
    )

    message = last_message(messages)

    try:
        res = json.loads(message)
    except json.decoder.JSONDecodeError:
        print("Error parsing JSON")
        print(message)
        return None

    out= []
    for o in res:
        o['file'] = src_path
        o['path'] = MagePath(o['path'])
        dep = Dependency(**o)
        out.append(dep )
    return DependencyTree( dependencies=out )


# convert( src_path, "nodejs", ".js" )
@app.command()
def recurse_through_dependencies(
    src_path = typer.Argument("examples/test_fizzbuzz.py" )
):
    dependencies:DependencyTree =get_dependencies(src_path)
    
    for dependency in dependencies.dependencies:
        if dependency.type == 'file':
            dependencies.append_tree( get_dependencies( dependency.path.normalized()) )

            #convert(dependency.path)

    return dependencies



if __name__ == "__main__":
    app()