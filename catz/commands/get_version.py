import sys
import click
import pkg_resources


@click.command(name='version', help='Display version info for catz')
def version():
    version = pkg_resources.require('catz')[0].version
    print('Version: {0}'.format(version))
    sys.exit(0)
