import os
from cx_Freeze import setup, Executable
from config.handler import set_version

build_exe_options = {
    'includes': [
        'utilities'
    ],
    'excludes': [
        'tkinter'
    ],
    'packages': [
        'pygments',
        'pyfiglet',
        'configargparse'
    ]
}

bdist_msi_options = {
    'upgrade_code': 'de0978d2-6462-41d4-a86f-69487bf35efa'
}

exe = Executable(
    script='app.py',
    targetName='jcat.exe'
)

version = os.environ.get('GITVERSION_SEMVER', '0.0.0')
set_version(version)

setup(
    name='jcat',
    version=version,
    description='A colourful syntax highlighting tool for your terminal.',
    options={
        'build_exe': build_exe_options,
        'bdist_msi': bdist_msi_options
    },
    executables=[exe]
)
