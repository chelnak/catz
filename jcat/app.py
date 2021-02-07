
import click
from click_default_group import DefaultGroup


from .commands import (
    get_content,
    list_lexers,
    list_themes,
    get_version
)


@click.group(cls=DefaultGroup, default='get', default_if_no_args=True)
@click.pass_context
def cli(ctx):
    pass


cli.add_command(get_content.get)
cli.add_command(list_lexers.lexers_group)
cli.add_command(list_themes.themes_group)
cli.add_command(get_version.version)


if __name__ == '__main__':
    cli()
