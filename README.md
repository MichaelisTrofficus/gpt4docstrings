<p align="center">
    <img alt="gpt4docstrings logo" src="images/logo.png" width=300 />
    <h1 align="center">gpt4docstrings</h1>
    <h3 align="center">Generating Python docstrings with OpenAI ChatGPT!!</h3>
</p>

---

[![PyPI](https://img.shields.io/pypi/v/gpt4docstrings.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gpt4docstrings.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gpt4docstrings)][python version]
[![License](https://img.shields.io/pypi/l/gpt4docstrings)][license]

[![Read the documentation at https://gpt4docstrings.readthedocs.io/](https://img.shields.io/readthedocs/gpt4docstrings/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/MichaelisTrofficus/gpt4docstrings/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/MichaelisTrofficus/gpt4docstrings/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/gpt4docstrings/
[status]: https://pypi.org/project/gpt4docstrings/
[python version]: https://pypi.org/project/gpt4docstrings
[read the docs]: https://gpt4docstrings.readthedocs.io/
[tests]: https://github.com/MichaelisTrofficus/gpt4docstrings/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/MichaelisTrofficus/gpt4docstrings
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## What is `gpt4docstrings`?

`gpt4docstrings` is a library that helps you to write docstrings
for your Python code. Select a path / paths where you want `gpt4docstrings`
to be applied and wait for the results!!

![](images/usage.gif)

## Requirements

`gpt4docstrings` supports Python 3.9 and above.

## Installation

You can install _gpt4docstrings_ via [pip] from [PyPI]:

```console
$ pip install gpt4docstrings
```

## Usage

##### Command Line Interface

The first option when using `gpt4docstrings` is to use it as a Command Line Interface (CLI).

The following is an example command that generates docstrings for all the non-documented
classes / functions under `src/` directory.

```bash
gpt4docstrings src/
```

Another quite common situation is that we want to exclude the `tests/` folder, for example,
from the generation of docstrings. Doing this is very simple.

```bash
gpt4docstrings --exclude tests/ .
```

Lastly, you could also run `gpt4docstrings` in a specific Python file.

```bash
gpt4docstrings ./src/example.py
```

Remember that, if you don't have your OpenAI API Key defined as an Environment Variable (OPENAI_API_KEY),
`gpt4docstrings` can accept the API Key as an option.

```bash
gpt4docstrings --exclude tests/ --api_key sk-xxxxxxxxxxxx .
```

##### pre-commit hook

Another cool use of `gpt4docstrings` is as a `precommit` hook.
All you have to do is add it to your configuration file and you’re done!

```yaml
repos:
  - repo: https://github.com/MichaelisTrofficus/gpt4docstrings
    rev: v0.1.0
    hooks:
      - id: gpt4docstrings
        name: gpt4docstrings
        language: python
        entry: gpt4docstrings
        types: [python]
```

Please see the [Command-line Reference] for more details!!

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_gpt4docstrings_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/MichaelisTrofficus/gpt4docstrings/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://gpt4docstrings.readthedocs.io/en/latest/license.html
[contributor guide]: https://gpt4docstrings.readthedocs.io/en/latest/contributing.html#
[command-line reference]: https://gpt4docstrings.readthedocs.io/en/latest/use_as_cli.html
