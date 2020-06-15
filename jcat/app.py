
from sys import exit
from rich.console import Console
from rich.syntax import Syntax
from utilities import lexers, validators, argument_handler, themes, path_handler


def cli():
    try:

        args = argument_handler.get_args()

        console = Console()
        console_theme = args.theme

        if args.list_themes is True:
            themes.get_themes()
            exit(0)

        if args.list_lexers is True:
            lexers.get_lexers()
            exit(0)

        lexer_name, data = path_handler.handle_input(args.filename)

        syntax = Syntax(data,
                        lexer_name,
                        theme=console_theme,
                        line_numbers=True)

        console.print(syntax)

    except Exception as e:
        raise e
        exit(1)


if __name__ == '__main__':
    cli()
