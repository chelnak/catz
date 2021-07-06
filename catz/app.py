
import click
from rich.console import Console
from click_default_group import DefaultGroup
from . import commands


@click.group(cls=DefaultGroup, default='get', default_if_no_args=True)
@click.pass_context
def cli(ctx):
    ctx.obj = Console()


# Root commands
cli.add_command(commands.get)
cli.add_command(commands.version)

# Groups
cli.add_command(commands.lexers)
cli.add_command(commands.themes)
