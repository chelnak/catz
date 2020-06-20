
import click
from sys import exit
from rich.console import Console
from rich.syntax import Syntax
from utilities import lexers, validators, themes
from handlers import input
from commands.lexers import list_lexers
from commands.themes import list_themes

@click.group()
def cli():
    pass


@cli.command()
@click.option('--theme', default='native', help='Override the default syntaxt highlighting theme. You can use jcat --list-themes to view a list of available themes.')
@click.option('--lexer', help='Override the lexer used when applying syntax highlighting. YOu can use jcat --list-lexers to view a list of available lexers.')
@click.argument('filename')
def main(theme, lexer, filename):
    try:

        console = Console()

        lexer_name, data = input.handle_input(filename, lexer)

        syntax = Syntax(data,
                        lexer_name,
                        theme=theme,
                        line_numbers=True)

        console.print(syntax)

    except Exception as e:
        raise e
        exit(1)


cli.add_command(list_lexers())
cli.add_command(list_themes())


if __name__ == '__main__':
    cli()
