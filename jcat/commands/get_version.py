import sys
import click
import pkg_resources


@click.command(name='version', help='Display version info for jcat')
def version():
    version = pkg_resources.require('jcat')[0].version
    print('Version: {0}'.format(version))
    sys.exit(0)
