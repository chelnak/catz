from rich.console import Console
from rich.table import Table
from pygments.styles import get_all_styles


def get_themes():

    styles = list(get_all_styles())
    table = Table(title='Console themes')
    table.add_column('Themes', style='cyan', no_wrap=True)

    for i in styles:
        table.add_row(i)

    console = Console()
    console.print(table)
