from sys import exit, argv
from configargparse import ArgumentParser, RawTextHelpFormatter
from config.handler import get_config, get_full_version

config = get_config()

description = '''
   _           _
  (_) ___ __ _| |_
  | |/ __/ _` | __|
  | | (_| (_| | |_
 _/ |\___\__,_|\__|
|__/

'''


def get_args():
    parser = ArgumentParser(
        prog=config['app_name'],
        description=description,
        formatter_class=RawTextHelpFormatter
    )

    parser.add(
        'filename',
        nargs='?',
        help='Path to the file that will be loaded'
    )

    parser.add(
        '--theme',
        dest='theme',
        env_var='JCAT_THEME',
        default='native',
        help='Override the default theme.'
    )

    parser.add(
        '--lexer',
        dest='lexer',
        env_var='JCAT_LEXER',
        help='Override the lexer. Useful for when jcat can\'t determine the correct lexer for syntax highlighting.'
    )

    parser.add(
        '--list-lexers',
        action='store_true',
        dest='list_lexers',
        help='List all available lexers'
    )

    parser.add(
        '--list-themes',
        action='store_true',
        dest='list_themes',
        help='List all available console themes'
    )

    parser.add(
        '--version',
        action='version',
        version=get_full_version()
    )

    if not len(argv) > 1:
        print(parser.format_help())
        exit(1)

    args = parser.parse_args()

    if (args.list_themes) and (args.list_lexers):
        print(parser.format_help())
        print('--list-themes and --list-lexers can\'t be used together')
        exit(1)

    return args
