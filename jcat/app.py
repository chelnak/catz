
from sys import exit
from rich.console import Console
from rich.syntax import Syntax
from utilities import lexers, validators, argument_handler


if __name__ == '__main__':

    console = Console()
    console_theme = 'monokai'

    try:

        args = argument_handler.get_args()

        with open(args.filename, 'r') as file:
            data = file.read()

            lexer_name = lexers.get_lexer(file.name)

            validators.validate(file.name, data)

            syntax = Syntax(data,
                            lexer_name,
                            theme=console_theme,
                            line_numbers=True)
            console.print(syntax)

    except FileNotFoundError:
        console.print_exception(theme=console_theme)
        exit(1)

    except Exception:
        console.print_exception(theme=console_theme)
        exit(1)
