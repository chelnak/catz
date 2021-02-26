import click
from rich.syntax import Syntax
from rich.table import Table
from pygments.styles import get_all_styles


@click.group(name='themes', help='Commands for working with themes.')
def themes_group():
    pass


@themes_group.command(name='list', help='List all available themes.')
@click.pass_obj
def list_themes(console):

    styles = list(get_all_styles())

    table = Table(title='Console themes')
    table.add_column('Themes', style='cyan', no_wrap=True)

    for i in styles:
        table.add_row(i)

    console.print(table)


@themes_group.command(name='show', help='Display examples of available themes')
@click.option('--name',
              '-n',
              default=None,
              help='''
              Display a named theme
              '''
              )
@click.pass_obj
def show_themes(console, name):

    styles = list(get_all_styles())

    data = '''
        def test_function(i):
            print(i)
    '''.strip()

    if name is not None:

        if name not in styles:
            raise click.ClickException(f'{name} is not a valid theme. Use catz themes list to view available themes')

        syntax_params = dict(
            code=data,
            lexer_name='python',
            theme=name,
            line_numbers=True
        )
        console.print(f'Theme: {name}')
        console.print(Syntax(**syntax_params))

    else:
        for i in styles:
            syntax_params = dict(
                code=data,
                lexer_name='python',
                theme=i,
                line_numbers=True
            )

            console.print(f'Theme: {i}')
            console.print(Syntax(**syntax_params))
