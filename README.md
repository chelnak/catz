[![Build Status](https://craigg.visualstudio.com/Pipelines/_apis/build/status/jcat?branchName=master)](https://craigg.visualstudio.com/Pipelines/_build/latest?definitionId=24&branchName=master)

# jcat :pencil:

A colourful syntax highlighting tool for your terminal.

`jcat` is powered by [rich](https://github.com/willmcgugan/rich) and [pygments](https://github.com/pygments/pygments). You can find a list of supported lexers [here](https://pygments.org/docs/lexers/).

## Usage

### Print a file with syntax highlighting

```PowerShell
jcat ./HelloWorld.ps1
```

!["HelloWorld"](media/HelloWorld.PNG)

### List available themes

```PowerShell
jcat --list-themes
```

### Print a file with syntax highlighting and override the default theme

```PowerShell
jcat ./HelloWorld.ps1 --theme vs
```

### Show the content of a file with syntax highlighting and override the default theme with an environment variable

```PowerShell
$ENV:JCAT_THEME="vs"
jcat ./HelloWorld.ps1
```

## Releasing

1. git tag -a vX.X.X -m "Release vX.X.X"
2. git push --follow-tags
