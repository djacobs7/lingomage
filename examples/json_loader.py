from pathlib import Path
import json
from rich import print
from rich.pretty import Pretty

EXAMPLE_JSON = '{"name": "John", "age": 30, "city": "New York"}'

def format_json(json_string: str):
    try:
        json_data = json.loads(json_string)
        formatted_json = json.dumps(json_data, indent=2)
        print(Pretty(formatted_json))
    except json.JSONDecodeError:
        print("[red]Invalid JSON[/red]")


format_json(EXAMPLE_JSON)