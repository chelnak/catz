import os
import urllib
import click
from urllib import parse, request

from pathlib import Path
from pygments.lexers import (
    get_lexer_for_filename,
    ClassNotFound,
    get_lexer_by_name, get_lexer_for_mimetype
)


def is_url(input):
    url = parse.urlparse(input)
    if url.netloc and url.scheme:
        return True


def get_content_from_url(url):

    VALID_PROTOCOLS = ['http', 'https']
    p = parse.urlparse(url).scheme
    if p not in VALID_PROTOCOLS:
        raise click.ClickException(f'{p} is not a valid http protocol.')

    try:
        with request.urlopen(url) as conn:
            content = conn.read().decode('utf-8')
            mime_type = conn.headers['content-type'].split(';')
            return content, mime_type
    except urllib.error.HTTPError as e:
        raise click.ClickException(e)


def get_content_from_file(file):

    try:

        resolved_path = os.path.expanduser(file) if file.startswith('~') else Path(file).resolve()

        with open(resolved_path, encoding='utf-8', errors='ignore') as file:
            data = file.read()
            filename = file.name

        return data, filename

    except OSError as e:
        raise click.ClickException(f'OSError: {e}')

    except FileNotFoundError:
        raise click.ClickException(f'FileNotFound: {file}')

    except UnicodeEncodeError as e:
        raise click.ClickException(f'Could not handle file encoding: {e}')


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
