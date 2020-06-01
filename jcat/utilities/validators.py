from sys import exit
from rich.console import Console
from pathlib import Path
from json import loads, JSONDecodeError

console = Console()


def validate(file_name, data):
    extension = Path(file_name).suffix

    try:
        if extension == '.json':
            loads(data)

    except JSONDecodeError as json_error:
        console.print('Failed to decode json file!\n{0}'.format(json_error),
                      style='red')
        exit(1)

    except Exception as e:
        console.print('A validation error occured!\n{0}'.format(e),
                      style='red')
        exit(1)
