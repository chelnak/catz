import click
from rich.console import Console
from urllib import parse
from .helpers import (
    get_lexer_from_filename,
    get_lexer_from_name,
    write_output,
    get_url,
    get_file
)


console = Console()


@click.command(name='get',
               help='Perform syntax highlighting on raw text from a local file or a url.'
               )
@click.argument('path')
@click.option('--theme',
              default='native',
              envvar='JCAT_THEME',
              help='''Override the default syntaxt highlighting theme.
              You can use jcat themes list to view a list of available themes.'''
              )
@click.option('--lexer',
              default=None,
              envvar='JCAT_LEXER',
              help='''Override the lexer used when applying syntax highlighting.
              You can use jcat lexers list to view a list of available lexers.'''
              )
def get(path, theme, lexer):

    url = parse.urlparse(path)

    if url.scheme:
        data, filename = get_url(path)
    else:
        data, filename = get_file(path)

    if lexer is not None:
        lexer_name = get_lexer_from_name(lexer)
    else:
        lexer_name = get_lexer_from_filename(filename)

    write_output(data, lexer_name, theme)
