import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "includes": [
        "jcat/utilities"
    ],
    "packages": [
        "pyfiglet"
    ]
}

bdist_msi_options = {}

exe = Executable(
    script="jcat/app.py",
    targetName="jcat.exe"
)

version = os.environ.get('GITVERSION__SEMVER).', '0.0-local')

setup(
    name="jcat",
    version=version,
    description="A colourful syntax highlighting tool for your terminal.",
    options={
        "build_exe": build_exe_options,
        'bdist_msi': bdist_msi_options},
    executables=[exe]
)
