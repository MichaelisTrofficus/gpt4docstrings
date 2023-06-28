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
    "-d",
    "--docstrings_style",
    type=click.STRING,
    default="google",
    help="Docstring style. Choose between `google`, `numpy` or `reStructuredText`",
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
        api_key=kwargs["api_key"],
    )
    docstrings_generator.generate_docstrings()
