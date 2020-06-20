
import click
from .commands.themes import list_themes
from .commands.lexers import list_lexers
from .commands.input import handle_input


@click.group()
@click.pass_context
def cli(ctx):
    pass


cli.add_command(handle_input.get)
cli.add_command(list_lexers.lexers_group)
cli.add_command(list_themes.themes_group)


if __name__ == '__main__':
    cli()
