import sys
import click
from rich.syntax import Syntax
from rich.console import Console
from .command_helpers import (
    get_lexer_from_filename,
    get_lexer_from_mimetype,
    get_lexer_from_name,
    get_content_from_url,
    get_content_from_file,
    is_url
)


@click.command(name='get',
               help='Perform syntax highlighting on raw text from a local file or a url.'
               )
@click.argument('path')
@click.option('--theme',
              '-t',
              default='native',
              envvar='CATZ_THEME',
              help='''Override the default syntaxt highlighting theme.
              You can use catz themes list to view a list of available themes.'''
              )
@click.option('--lexer',
              '-l',
              default=None,
              envvar='CATZ_LEXER',
              help='''Override the lexer used when applying syntax highlighting.
              You can use catz lexers list to view a list of available lexers.'''
              )
@click.option('--passthru',
              '-p',
              is_flag=True,
              envvar='CATZ_PASSTHRU',
              help='''Pass the content of the file directly to stdout with no lexer applied.'''
              )
def get(path, theme, lexer, passthru):

    data, lexer_identifier = get_content_from_url(
        path) if is_url(path) else get_content_from_file(path)

    if passthru:
        print(data, file=sys.stdout)
        return

    lexer_name = get_lexer_from_name(lexer) if lexer is not None else get_lexer_from_mimetype(
        lexer_identifier) if is_url(path) else get_lexer_from_filename(lexer_identifier)

    console = Console()
    console.print(Syntax(data, lexer_name, theme=theme, line_numbers=True))
