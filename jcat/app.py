
import click
import sys
from . import VERSION
from .commands.themes import list_themes
from .commands.lexers import list_lexers
from .commands.input import handle_input


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command(name='version', help='Display version info for jcat')
def get_version():
    print('Version: {0}'.format(VERSION))
    sys.exit(0)


cli.add_command(handle_input.get)
cli.add_command(list_lexers.lexers_group)
cli.add_command(list_themes.themes_group)


if __name__ == '__main__':
    cli()
