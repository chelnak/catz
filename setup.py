import os
from setuptools import setup


PRODUCT_NAME = 'catz'
DEPENDENCIES = [
    'rich==9.10.0',
    'click==7.1.2',
    'click-default-group==1.2.2'
]
VERSION = os.environ.get('GITVERSION_MAJORMINORPATCH', '0.0.3')

setup(
    name=PRODUCT_NAME,
    version=VERSION,
    author='chelnak',
    description='A colourful syntax highlighting tool for your terminal.',
    url='https://github.com/chelnak/catz',
    packages=['catz', 'catz.commands'],
    entry_points={
        'console_scripts': ['catz = catz.app:cli']
    },
    install_requires=DEPENDENCIES,
    test_suite='nose.collector',
    tests_require=['nose'],
)
