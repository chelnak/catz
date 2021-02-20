# catz :pencil:

A colourful syntax highlighting tool for your terminal.

`catz` is powered by [rich](https://github.com/willmcgugan/rich) and [pygments](https://github.com/pygments/pygments).

## Supported filetypes

`catz` supports all of the lexers provided by pygments. You can find a full list [here](https://pygments.org/docs/lexers/).

## Install

Install the latest release from the Releases page or run the following:

```PowerShell
pip install catz
```

## Usage

File content syntax highlighting

```PowerShell
catz ./tests/terraform.tf
```

### Url content syntax highlighting

```PowerShell
catz https://raw.githubusercontent.com/chelnak/catz/master/README.md
```

### Override the default theme

```PowerShell
catz ./HelloWorld.ps1 --theme vs
```

### Set the theme with an environment variable

```PowerShell
$ENV:CATZ_THEME="vs"
catz ./HelloWorld.ps1
```

### Set the lexer with an environment variable

```PowerShell
$ENV:CATZ_LEXER="html"
catz get ./HelloWorld.ps1
```

### Passthrough

```PowerShell
catz ./HelloWorld.ps1 --passthru
```

```PowerShell
catz ./HelloWorld.ps1 --passthru >> output.txt
```

### Line highlighting

Highlight individual lines

```PowerShell
catz ./HelloWorld.ps1 --highlight 1,4
```

Highlight a range of lines

```PowerShell
catz ./HelloWorld.ps1 -highlight 1-4
```

### List available themes

```PowerShell
catz themes list
```

### Display examples of available themes

```PowerShell
catz themes show
```

```PowerShell
catz themes show --name vim
```

### List available lexers

```PowerShell
catz lexers list
```

## Releasing

1. git tag -a vX.X.X -m "Release vX.X.X"
2. git push --follow-tags
