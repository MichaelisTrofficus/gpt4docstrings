import os

import click

import gpt4docstrings


@click.option(
    "-m",
    "--model",
    type=click.STRING,
    default="gpt-3.5-turbo",
    help="The model to be used by `gpt4docstrings`. By default, `gpt-3.5-turbo`.",
)
@click.option(
    "-s",
    "--style",
    type=click.STRING,
    default="google",
    help="Docstring style, which must be one of 'google', 'reStructuredText', 'epytext', 'numpy'",
)
@click.option(
    "-k",
    "--api_key",
    type=click.STRING,
    default="",
    help="OpenAI's API key. If not provided, `gpt4docstrings` will try to access `OPENAI_API_KEY` environment variable.",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    type=click.Path(
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    default=(),
    help="Exclude PATHs of files and/or directories. Multiple `-e/--exclude` invocations supported.",
)
@click.option(
    "-v",
    "--verbose",
    type=click.INT,
    default=0,
    help="Verbosity parameter. Defaults to 0.",
)
@click.help_option("-h", "--help")
@click.argument(
    "paths",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
    is_eager=True,
    nargs=-1,
)
@click.command()
def main(paths, **kwargs):
    if not paths:
        paths = (os.path.abspath(os.getcwd()),)

    docstrings_generator = gpt4docstrings.GPT4Docstrings(
        paths=paths,
        excluded=kwargs["exclude"],
        model=kwargs["model"],
        docstring_style=kwargs["style"],
        api_key=kwargs["api_key"],
        verbose=kwargs["verbose"],
    )
    docstrings_generator.generate_docstrings()
