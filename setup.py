import os
from setuptools import setup


PRODUCT_NAME = 'jcat'
DEPENDENCIES = [
    'rich==1.3.0',
    'click==7.1.2',
    'requests==2.25.1',
    'click-default-group==1.2.2'
]
VERSION = os.environ.get('GITVERSION_MAJORMINORPATCH', '0.0.3')


setup(
    name=PRODUCT_NAME,
    version=VERSION,
    author='chelnak',
    author_email='chelnak@github',
    description='A colourful syntax highlighting tool for your terminal.',
    url='https://github.com/chelnak/jcat',
    packages=['jcat', 'jcat.commands'],
    entry_points={
        'console_scripts': ['jcat = jcat.app:cli']
    },
    install_requires=DEPENDENCIES
)
