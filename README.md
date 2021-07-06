# catz :pencil:

A colourful syntax highlighting tool for your terminal.

`catz` is powered by [rich](https://github.com/willmcgugan/rich) and [pygments](https://github.com/pygments/pygments).

## Supported filetypes

`catz` supports all of the lexers provided by pygments. You can find a full list [here](https://pygments.org/docs/lexers/).

## Install

Install the latest release from the Releases page or run the following:

```bash
pip install catz
```

## Usage

File content syntax highlighting

```bash
catz ./tests/terraform.tf
```

### Override the default theme

```bash
catz ./HelloWorld.ps1 --theme vs
```

### Passthrough

```bash
catz ./HelloWorld.ps1 --passthru
```

```bash
catz ./HelloWorld.ps1 --passthru >> output.txt
```

### Line highlighting

Highlight individual lines

```bash
catz ./HelloWorld.ps1 --highlight 1,4
```

Highlight a range of lines

```bash
catz ./HelloWorld.ps1 -highlight 1-4
```

### List available themes

```bash
catz themes list
```

### Display examples of available themes

```bash
catz themes show
```

```bash
catz themes show --name vim
```

### List available lexers

```bash
catz lexers list
```

## Releasing

1. git tag -a vX.X.X -m "Release vX.X.X"
2. git push --follow-tags
