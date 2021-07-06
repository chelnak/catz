import sys
import click
from rich.syntax import Syntax
from .util import (
    get_lexer_from_filename,
    get_lexer_from_name
)


class HandleRangeInput(click.Option):
    """
    Override to handle different types of line number inputs for
    --highlight / -hl.

    Accepts a csv of numbers (1,2,6) or a range (1-6).
    """
    def consume_value(self, ctx, opts):
        value = super().consume_value(ctx, opts)
        highlight_exception_base = 'Invalid value for --highlight / -hl:'

        if value is not None:

            try:

                if '-' in value:
                    input_list = value.split('-')

                    if len(input_list) > 2:
                        raise click.ClickException(
                            f'{highlight_exception_base} Could not convert {value} to a valid range')

                    input_list = list(map(int, input_list))

                    if input_list[0] > input_list[1]:
                        raise click.ClickException(
                            f'{highlight_exception_base} {input_list[0]} is greater than {input_list[1]}')

                    value = list(range(input_list[0], input_list[1]+1))

                    if len(value) == 0:
                        value = input_list[0]

                else:
                    value = list(map(int, value.split(',')))

            except ValueError as e:
                raise click.ClickException(
                    f'{highlight_exception_base} {e} is not a valid integer range')

        return value


@click.command(name='get',
               help='Perform syntax highlighting on raw text from a local file.',
               no_args_is_help=True
               )
@click.argument('file', type=click.File(mode='r', encoding='utf-8', errors='ignore'), default=sys.stdin)
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
@click.option('--highlight',
              '-hl',
              default=None,
              cls=HandleRangeInput,
              help='''Highlight specific lines in the parsed file.
              Accepts a comma separated list of line numbers.
              '''
              )
@click.option('--passthru',
              '-p',
              is_flag=True,
              envvar='CATZ_PASSTHRU',
              help='''Pass the content of the file directly to stdout with no lexer applied.'''
              )
@click.pass_obj
def get(console, file, theme, lexer, highlight, passthru):

    data = file.read()

    if passthru:
        print(data, file=sys.stdout)
        return

    filename = file.name

    if lexer is None:
        _lexer = get_lexer_from_filename(filename)
    else:
        _lexer = get_lexer_from_name(lexer)

    syntax_params = {
        'code': data,
        'lexer_name': _lexer,
        'theme': theme,
        'line_numbers': True
    }

    if highlight is not None:
        syntax_params['highlight_lines'] = set(highlight)

    console.print(Syntax(**syntax_params))
