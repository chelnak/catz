import os
from setuptools import find_packages, setup


PRODUCT_NAME = 'jcat'
DEPENDENCIES = []
VERSION = os.environ.get('GITVERSION_MAJORMINORPATCH', '0.0.0')


setup(
    name=PRODUCT_NAME,
    version=VERSION,
    author='chelnak',
    author_email='chelnak@github',
    description='A colourful syntax highlighting tool for your terminal.',
    url='https://github.com/chelnak/jcat',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['jcat = jcat.app:cli']
    },
    install_requires=DEPENDENCIES
)
