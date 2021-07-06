from pygments.lexers import (
    get_lexer_for_filename,
    get_lexer_by_name,
    ClassNotFound
)


def get_lexer_from_filename(filename):
    """
    Internal function to gracefully search for a lexer
    by filename.
    """
    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.name
    except ClassNotFound:
        pass


def flatten(input):
    """
    Flattern a list.
    """
    return ','.join([x for x in input])


def get_lexer_from_name(name):
    """
    Get lexer by name
    """
    try:
        lexer = get_lexer_by_name(name)
        return lexer.name
    except ClassNotFound:
        pass
