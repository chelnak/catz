import sys
import click
from urllib import parse
from .command_helpers import (
    get_lexer_from_filename,
    get_lexer_from_name,
    write_output,
    get_url,
    get_file
)


@click.command(name='get',
               help='Perform syntax highlighting on raw text from a local file or a url.'
               )
@click.argument('path')
@click.option('--theme',
              default='native',
              envvar='CATZ_THEME',
              help='''Override the default syntaxt highlighting theme.
              You can use catz themes list to view a list of available themes.'''
              )
@click.option('--lexer',
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

    url = parse.urlparse(path)

    if url.scheme:
        data, filename = get_url(path)
    else:
        data, filename = get_file(path)

    if passthru:
        print(data, file=sys.stdout)
    else:
        if lexer is not None:
            lexer_name = get_lexer_from_name(lexer)
        else:
            lexer_name = get_lexer_from_filename(filename)
        write_output(data, lexer_name, theme)
