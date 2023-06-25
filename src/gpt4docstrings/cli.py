import os

import click

import gpt4docstrings


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
    help=(
        "Exclude PATHs of files and/or directories. Multiple `-e/--exclude` "
        "invocations supported."
    ),
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
    )
    docstrings_generator.generate_docstrings()
