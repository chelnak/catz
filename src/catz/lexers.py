from __future__ import annotations

from typing import Any

from pygments.lexers import (
    ClassNotFound,
    get_all_lexers,
    get_lexer_by_name,
    get_lexer_for_filename,
)
from rich import box
from rich.console import Console
from rich.table import Table


def get_lexer_from_filename(filename: str) -> str | None:
    """Internal function to gracefully search for a lexer by filename.

    Args:
        filename (str): The filename to search for.

    Returns:
        str | None: The lexer name if found, otherwise None.
    """

    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.name.lower()
    except ClassNotFound:
        return None


def get_lexer_from_name(name: str) -> str | None:
    """Get lexer by name.

    Args:
        name (str): The name of the lexer.

    Returns:
        str: The lexer name.
    """

    try:
        lexer = get_lexer_by_name(name)
        return lexer.name.lower()
    except ClassNotFound:
        return None


def list_lexers() -> None:
    """List all available lexers."""

    console = Console()
    lexers = get_all_lexers()

    table = Table(title="Lexers", box=box.SQUARE)
    table.add_column("Name", no_wrap=True)
    table.add_column("Short Names", no_wrap=True)
    table.add_column("File Types", no_wrap=True)

    for i in lexers:
        table.add_row(i[0], ",".join(i[1]), ",".join(i[2]))

    console.print(table)


if __name__ == "__main__":
    list_lexers()
