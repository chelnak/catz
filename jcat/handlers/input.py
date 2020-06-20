import requests
import sys
import os
from rich.console import Console
from urllib import parse
from pathlib import Path
from utilities import lexers

VALID_PROTOCOLS = ['http', 'https']
VALID_STATUS_CODES = [200]

console = Console()


def resolve_path(path):
    # Handle file paths
    if path.startswith('~'):
        return os.path.expanduser(path)
    else:
        return Path(path).resolve()


def handle_input(path, lexer=None):
    url = parse.urlparse(path)

    if url.scheme:

        if url.scheme not in VALID_PROTOCOLS:
            console.print('{0} is not a valid protocol'.format(url.scheme),
                          style='red')
            sys.exit(1)

        r = requests.get(path)

        if r.status_code not in VALID_STATUS_CODES:
            console.print('Request failed!\n{0}'.format(r.text),
                          style='red')
            sys.exit(1)

        data = r.text
        filename = parse.urlsplit(path).path.split('/')[-1]

    else:
        try:
            resolved_path = resolve_path(path)
            with open(resolved_path, 'r') as file:
                data = file.read()
                filename = file.name

        except FileNotFoundError:
            console.print_exception()
            exit(1)

    l = lexer if lexer is not None else filename
    lexer_name = lexers.get_lexer(l)
    return lexer_name, data
