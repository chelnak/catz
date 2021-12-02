from __future__ import annotations

import sys
from typing import TextIO

import click
from rich.align import Align
from rich.console import Console, Group
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text

from . import __version__
from .languages import get_lexer_from_filename, get_lexer_from_name
from .options import RangeInputOption


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
    "--style",
    "-s",
    default="solarized-dark",
    help="Override the default syntaxt highlighting style. For a list of styles visit https://pygments.org/styles or run python -m catz.styles.",
)
@click.option(
    "--language",
    "-l",
    help="Override the language used when applying syntax highlighting. For a list of languages visit https://pygments.org/languages or run python -m catz.languages.",
)
@click.option(
    "--highlight",
    "-hl",
    cls=RangeInputOption,
    type=set[int],
    help="Highlight specific lines in the parsed file. Accepts a comma separated list (e.g. 1,2,3,4,5) or a range (e.g 1-5) of line numbers.",
)
@click.option(
    "--line-range",
    "-lr",
    type=click.types.Tuple([int, int]),
    help="Only display a range of lines in the file. Accepts two integers separated by a space (e.g. 1 5).",
)
@click.option(
    "--indent-guides",
    is_flag=True,
    help="Display indentation guides.",
)
@click.version_option(__version__)
def main(
    file: TextIO,
    style: str,
    language: str,
    highlight: set[int],
    line_range: tuple[int, int],
    indent_guides: bool,
) -> None:
    """Perform syntax highlighting on raw text from a local file or stdin.

    Args:
        file (TextIO): The file object to read from.
        style (str): The style to use for syntax highlighting.
        language (str): The language to use for syntax highlighting.
        highlight (set[int]): The lines to highlight.
        line_range (tuple[int,int]): The lines to show.
        indent_guides (bool): Display indentation guides.
    """

    console = Console()
    data = file.read()

    if not click.get_text_stream("stdout").isatty():
        print(data, file=sys.stdout)
        return

    if not language:
        _language = get_lexer_from_filename(file.name)
    else:
        _language = get_lexer_from_name(language)

    title = Text(f"path: {file.name}", style=Style(dim=True), justify="center")
    sub_title = Text(
        f"type: {_language or 'unknown'}", style=Style(dim=True), justify="center"
    )
    group = Group(
        Panel(
            Align.center(Group(title, sub_title), vertical="middle"),
            padding=(1),
            border_style=Style(dim=True),
        ),
        Padding(
            Syntax(
                code=data,
                lexer_name=_language or "",
                theme=style,
                line_numbers=True,
                background_color="default",
                highlight_lines=highlight,
                line_range=line_range,
                indent_guides=indent_guides,
            ),
            pad=(1, 0, 1, 0),
        ),
    )

    console.print(group)
