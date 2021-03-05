import click
import difflib
from rich.syntax import Syntax


@click.command(name='diff',
               help='Get the diff between two files.',
               no_args_is_help=True
               )
@click.argument('ref', required=True)
@click.argument('diff', required=True)
@click.option('--theme',
              '-t',
              default='native',
              envvar='CATZ_THEME',
              help='''Override the default syntaxt highlighting theme.
              You can use catz themes list to view a list of available themes.'''
              )
@click.pass_obj
def diff(console, ref, diff, theme):

    try:
        with open(file=ref, mode='r') as r:
            with open(file=diff, mode='r') as d:
                diff = difflib.ndiff(r.readlines(), d.readlines())

                syntax_params = dict(
                    code=''.join(list(diff)),
                    lexer_name='bash',
                    theme=theme,
                    line_numbers=False
                )

                console.print(Syntax(**syntax_params))

    except FileNotFoundError as e:
        raise click.ClickException(f'{e}')
