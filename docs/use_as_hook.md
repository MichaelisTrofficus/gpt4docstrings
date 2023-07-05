# Use `gpt4docstrings` as pre-commit hook

Another cool use of `gpt4docstrings` is as a precommit hook.
All you have to do is add it to your configuration file and you're done!

```yaml
repos:
  - repo: https://github.com/MichaelisTrofficus/gpt4docstrings
    rev: v0.0.5
    hooks:
      - id: gpt4docstrings
        name: gpt4docstrings
        language: python
        entry: gpt4docstrings
        types: [python]
```
