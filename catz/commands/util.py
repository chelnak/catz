import os
import urllib
import click
from urllib import parse, request
from pathlib import Path
from pygments.lexers import (
    get_lexer_for_filename,
    get_lexer_by_name,
    get_lexer_for_mimetype,
    ClassNotFound
)


def __get_lexer_from_mimetype(mimetype):
    """
    Internal function to gracefully search for a lexer
    by mime type.
    """
    try:
        lexer = get_lexer_for_mimetype(mimetype)
        return lexer.name
    except ClassNotFound:
        pass


def __get_lexer_from_filename(filename):
    """
    Internal function to gracefully search for a lexer
    by filename.
    """
    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.name
    except ClassNotFound:
        pass


def flatten(input):
    """
    Flattern a list.
    """
    return ','.join([x for x in input])


def is_url(input):
    """
    Test if the given input is a valid URL
    """
    url = parse.urlparse(input)
    if url.netloc and url.scheme:
        return True


def get_content_from_url(url):
    """
    Retrieve content from a url.

    Returns the raw data and a lexer if one can be found.
    """
    VALID_PROTOCOLS = ['http', 'https']
    p = parse.urlparse(url).scheme
    if p not in VALID_PROTOCOLS:
        raise click.ClickException(f'{p} is not a valid http protocol.')

    try:
        with request.urlopen(url) as conn:
            content = conn.read().decode('utf-8')
            mime_type = conn.headers['content-type'].split(';')
            lexer = __get_lexer_from_mimetype(mime_type)
            return content, lexer

    except urllib.error.HTTPError as e:
        raise click.ClickException(e)


def get_content_from_file(file):
    """
    Retrieve content from a file.

    Returns the raw data and a lexer if one can be found.
    """
    try:

        resolved_path = os.path.expanduser(
            file) if file.startswith('~') else Path(file).resolve()

        with open(resolved_path, encoding='utf-8', errors='ignore') as file:
            data = file.read()
            filename = file.name
        lexer = __get_lexer_from_filename(filename)
        return data, lexer

    except OSError as e:
        raise click.ClickException(f'OSError: {e}')

    except FileNotFoundError:
        raise click.ClickException(f'FileNotFound: {file}')

    except UnicodeEncodeError as e:
        raise click.ClickException(f'Could not handle file encoding: {e}')


def get_lexer_from_name(name):
    """
    Get lexer by name
    """
    try:
        lexer = get_lexer_by_name(name)
        return lexer.name
    except ClassNotFound:
        pass
