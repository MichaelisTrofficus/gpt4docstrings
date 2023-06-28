# Usage

## Use `gpt4docstrings` as CLI

```{eval-rst}
.. click:: gpt4docstrings.cli:main
    :prog: gpt4docstrings
    :nested: full
```

## Use `gpt4docstrings` as pre-commit hook

It is better to choose this option since we can
concatenate `gpt4docstrings` with `black` to
format the docstrings (sometimes docstrings may
appear with a wrong format).

```yaml
repos:
  - repo: https://github.com/MichaelisTrofficus/gpt4docstrings
    rev: c74a1a3ec68b73f1c8c543ecf387850341d3876b
    hooks:
      - id: gpt4docstrings
        name: gpt4docstrings
        language: python
        entry: gpt4docstrings
        types: [python]
  - repo: local
    hooks:
      - id: black
        name: black
        entry: black
        language: system
        types: [python]
```
