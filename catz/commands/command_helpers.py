import os
import requests
import sys
from pathlib import Path
from urllib import parse
from rich.syntax import Syntax
from rich.console import Console
from pygments.lexers import (
    get_lexer_for_filename,
    ClassNotFound,
    get_lexer_by_name
)


console = Console()


def resolve_path(path):
    # Handle file paths
    if path.startswith('~'):
        return os.path.expanduser(path)
    else:
        return Path(path).resolve()


def get_url(url):

    VALID_PROTOCOLS = ['http', 'https']
    VALID_STATUS_CODES = [200]

    parsed_url = parse.urlparse(url)

    if parsed_url.scheme not in VALID_PROTOCOLS:
        console.print('{0} is not a valid protocol'.format(parsed_url.scheme), style='red')
        sys.exit(1)

    r = requests.get(url)

    if r.status_code not in VALID_STATUS_CODES:
        console.print('Request failed!\n{0}'.format(r.text), style='red')
        sys.exit(1)

    data = r.text
    filename = parse.urlsplit(url).path.split('/')[-1]

    return data, filename


def get_file(file):

    try:
        resolved_path = resolve_path(file)
        with open(resolved_path, encoding='utf8') as file:
            data = file.read()
            filename = file.name
        return data, filename

    except FileNotFoundError:
        console.print_exception()
        exit(1)


def write_output(data, lexer_name, theme):

    syntax = Syntax(data,
                    lexer_name,
                    theme=theme,
                    line_numbers=True)
    console.print(syntax)


def get_lexer_from_filename(name):

    try:
        lexer = get_lexer_for_filename(name)
        return lexer.name
    except ClassNotFound:
        console.print(
            'WARNING: Could not determine correct lexer for this file!',
            style='yellow'
        )
        return ''


def get_lexer_from_name(name):

    try:
        lexer = get_lexer_by_name(name)
        return lexer.name
    except ClassNotFound:
        console.print(
            'WARNING: Could not determine correct lexer for {0}!'.format(name),
            style='yellow'
        )
        return ''
