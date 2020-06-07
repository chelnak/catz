from sys import exit, argv
from configargparse import ArgumentParser, RawTextHelpFormatter
from jcat.config.handler import get_config, get_full_version

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

    return args
