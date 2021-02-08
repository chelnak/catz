import os
import requests
import click
from urllib import parse
from pathlib import Path
from pygments.lexers import (
    get_lexer_for_filename,
    ClassNotFound,
    get_lexer_by_name, get_lexer_for_mimetype
)


def is_url(input):
    url = parse.urlparse(input)
    if url.scheme:
        return True


def get_content_from_url(url):

    VALID_PROTOCOLS = ['http', 'https']

    parsed_url = parse.urlparse(url)

    if parsed_url.scheme not in VALID_PROTOCOLS:
        raise click.ClickException(f'{parsed_url.scheme} is not a valid http protocol.')

    try:
        response = requests.get(url)
        mime_type = response.headers['content-type'].split(';')
        response.raise_for_status()
        return response.text, mime_type
    except requests.exceptions.RequestException as e:
        raise click.ClickException(e)


def get_content_from_file(file):

    try:

        resolved_path = os.path.expanduser(file) if file.startswith('~') else Path(file).resolve()

        with open(resolved_path, encoding='utf8') as file:
            data = file.read()
            filename = file.name

        return data, filename

    except FileNotFoundError:
        raise click.ClickException(f'FileNotFound: {file}')


def get_lexer_from_mimetype(mimetype):

    try:
        lexer = get_lexer_for_mimetype(mimetype)
        return lexer.name
    except ClassNotFound:
        pass


def get_lexer_from_filename(filename):

    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.name
    except ClassNotFound:
        pass


def get_lexer_from_name(name):

    try:
        lexer = get_lexer_by_name(name)
        return lexer.name
    except ClassNotFound:
        pass
