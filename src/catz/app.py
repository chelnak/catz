import sys
from json import loads
from typing import TextIO

import click
from rich.align import Align
from rich.console import Console, Group
from rich.padding import Padding
from rich.panel import Panel
from rich.repr import T
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from . import __version__
from .lexers import get_lexer_from_filename, get_lexer_from_name
from .range import RangeInput


@click.command(
    help="Perform syntax highlighting on raw text from a local file.",
    no_args_is_help=True,
)
@click.argument(
    "file",
    type=click.File(mode="r", encoding="utf-8", errors="ignore"),
    default=sys.stdin,
)
@click.option(
    "--theme",
    "-t",
    default="native",
    help="""Override the default syntaxt highlighting theme.
              You can use catz themes list to view a list of available themes.""",
)
@click.option(
    "--lexer",
    "-l",
    help="""Override the lexer used when applying syntax highlighting.
              You can use catz lexers list to view a list of available lexers.""",
)
@click.option(
    "--highlight",
    "-hl",
    cls=RangeInput,
    help="""Highlight specific lines in the parsed file.
              Accepts a comma separated list of line numbers.
              """,
)
@click.version_option(__version__)
def main(file: TextIO, theme: str, lexer: str, highlight: str) -> None:
    """Perform syntax highlighting on raw text from a local file or stdin.

    Args:
        file: The file object to read from.
        theme: The theme to use for syntax highlighting.
        lexer: The lexer to use for syntax highlighting.
        highlight: The lines to highlight.
    """
    console = Console()
    data = file.read()
    _highlight = set(loads(highlight)) if highlight else None
    filename = file.name

    if not click.get_text_stream("stdout").isatty():
        print(data, file=sys.stdout)
        return

    if not lexer:
        _lexer = get_lexer_from_filename(filename)
    else:
        _lexer = get_lexer_from_name(lexer)

    group = Group(
        Panel(
            Align.center(Text(file.name, style=Style(dim=True)), vertical="middle"),
            padding=(1),
            border_style=Style(dim=True),
        ),
        Padding(
            Syntax(
                code=data,
                lexer_name=_lexer or "",
                theme=theme,
                line_numbers=True,
                background_color="default",
                highlight_lines=_highlight,
            ),
            pad=(1, 0, 0, 0),
        ),
    )

    console.print(group)
