# Command Line Interface (CLI)

The first option when using `gpt4docstrings` is to use it as a Command Line Interface (CLI).
The options available for the CLI can be seen below.

```{eval-rst}
.. click:: gpt4docstrings.cli:main
    :prog: gpt4docstrings
    :nested: full
```

The following is an example command that generates docstrings for all the non-documented
classes / functions under `src/` directory.

```shell
gpt4docstrings src/
```

Another quite common situation is that we want to exclude the `tests/` folder, for example,
from the generation of docstrings. Doing this is very simple.

```shell
gpt4docstrings --exclude tests/ .
```

If you don't have your OpenAI API Key defined as a Environment Variable (`OPENAI_API_KEY`), `gpt4docstrings`
can accept the API Key as an option.

```shell
gpt4docstrings --exclude tests/ --api_key sk-xxxxxxxxxxxx .
```
