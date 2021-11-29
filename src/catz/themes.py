from pygments.styles import get_all_styles
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.syntax import Syntax
from rich.table import Table


def show_themes() -> None:
    """Display examples of available themes."""

    console = Console()
    styles = list(get_all_styles())
    data = "def test_function(i):\n\tprint(i)".strip()

    table = Table(title="Themes", box=box.SQUARE)
    table.add_column("Name", justify="left")
    table.add_column("Example", justify="left")

    for i in styles:

        table.add_row(
            i,
            Padding(
                Syntax(
                    code=data,
                    lexer_name="python",
                    theme=i,
                    background_color="default",
                ),
                pad=(0, 0, 3, 0),
            ),
        )

    console.print(table)


if __name__ == "__main__":
    show_themes()
