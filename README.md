[![Build Status](https://craigg.visualstudio.com/Pipelines/_apis/build/status/jcat?branchName=master)](https://craigg.visualstudio.com/Pipelines/_build/latest?definitionId=24&branchName=master)

# jcat :pencil:

A colourful syntax highlighting tool for your terminal.

`jcat` is powered by [rich](https://github.com/willmcgugan/rich) and [pygments](https://github.com/pygments/pygments).

## Supported filetypes

`jcat` supports all of the lexers provided by pygments. You can find a full list [here](https://pygments.org/docs/lexers/).

## Install

Install the latest release from the Releases page or run the following:

```PowerShell
pip install jcat
```

## Usage

### Print a file with syntax highlighting

```PowerShell
jcat ./tests/terraform.tf
```

### Print a url with syntax highlighting

```PowerShell
jcat https://raw.githubusercontent.com/chelnak/jcat/master/README.md
```

### List available themes

```PowerShell
jcat themes list
```

### List available lexers

```PowerShell
jcat lexers list
```

### Print a file with syntax highlighting and override the default theme

```PowerShell
jcat ./HelloWorld.ps1 --theme vs
```

### Set the theme with an environment variable

```PowerShell
$ENV:JCAT_THEME="vs"
jcat ./HelloWorld.ps1
```

### Set the lexer with an environment variable

```PowerShell
$ENV:JCAT_lexer="html"
jcat get ./HelloWorld.ps1
```

### Passthrough to stdout

```PowerShell
jcat ./HelloWorld.ps1 -passthru
```

```PowerShell
jcat ./HelloWorld.ps1 -passthru >> output.txt
```

## Releasing

1. git tag -a vX.X.X -m "Release vX.X.X"
2. git push --follow-tags
