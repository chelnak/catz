from rich.console import Console
from rich.table import Table
from pygments.lexers import get_all_lexers, get_lexer_for_filename, ClassNotFound, get_lexer_by_name, get_lexer_for_mimetype
from utilities import argument_handler

console = Console()


def flatten(t):
    return ','.join([x for x in t])


def get_lexers():

    lexers = get_all_lexers()

    table = Table(title='Available Lexers')
    table.add_column('Name', style='cyan', no_wrap=True)
    table.add_column('Short Names', style='cyan', no_wrap=True)
    table.add_column('File Types', style='cyan', no_wrap=True)
    table.add_column('Mime Types', style='cyan', no_wrap=True)

    for i in lexers:
        table.add_row(i[0], flatten(i[1]), flatten(i[2]), flatten(i[3]))

    console = Console()
    console.print(table)


def get_lexer(file_name):

    args = argument_handler.get_args()

    try:
        if (args.lexer):
            lexer = get_lexer_by_name(args.lexer)
        else:
            lexer = get_lexer_for_filename(file_name)

        return lexer.name
    except ClassNotFound:
        console.print(
            'WARNING: Could not determine correct lexer for this file!',
            style='yellow'
        )
        return ''
