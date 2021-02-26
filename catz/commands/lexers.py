import click
from rich.console import Console
from rich.table import Table
from pygments.lexers import get_all_lexers
from .util import flatten


@click.group(name='lexers', help='Commands for working with lexers.')
def lexers_group():
    pass


@lexers_group.command(name='list', help='List all available lexers.')
@click.pass_obj
def list_lexers(coneole):

    lexers = get_all_lexers()

    table = Table(title='Available Lexers')
    table.add_column('Name', style='cyan', no_wrap=True)
    table.add_column('Short Names', style='cyan', no_wrap=True)
    table.add_column('File Types', style='cyan', no_wrap=True)

    for i in lexers:
        table.add_row(i[0], flatten(i[1]), flatten(i[2]))

    console = Console()
    console.print(table)
