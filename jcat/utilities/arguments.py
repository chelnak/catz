from sys import exit, argv
import pyfiglet
from configargparse import ArgParser, RawTextHelpFormatter


def get_args():
    name = pyfiglet.figlet_format('jcat')
    parser = ArgParser(
        prog='jcat', description=name,
        formatter_class=RawTextHelpFormatter
    )
    parser.add(
        "filename",
        help='Path to the file that will be loaded'
    )

    if not len(argv) > 1:
        print(parser.format_help())
        exit(1)

    args = parser.parse_args()

    return args
