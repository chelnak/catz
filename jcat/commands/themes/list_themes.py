import click
from rich.console import Console
from rich.table import Table
from pygments.styles import get_all_styles


@click.group(name='themes', help='Commands for working with themes.')
def themes_group():
    pass


@themes_group.command(name='list', help='List all available themes.')
def list_themes():

    styles = list(get_all_styles())
    table = Table(title='Console themes')
    table.add_column('Themes', style='cyan', no_wrap=True)

    for i in styles:
        table.add_row(i)

    console = Console()
    console.print(table)
