from rich.console import Console
from pygments.lexers import get_lexer_for_filename, ClassNotFound

console = Console()


def get_lexer(file_name):
    try:
        lexer = get_lexer_for_filename(file_name)
        return lexer.name
    except ClassNotFound:
        console.print(
            'WARNING: Could not determine correct lexer for this file!',
            style='yellow'
        )
        return ''
