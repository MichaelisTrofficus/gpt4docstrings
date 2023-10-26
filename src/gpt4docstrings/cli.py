import os

import click

import gpt4docstrings
from gpt4docstrings.config import GPT4DocstringsConfig


@click.option(
    "-m",
    "--model",
    type=click.STRING,
    default="gpt-3.5-turbo",
    help="The model to be used by `gpt4docstrings`. By default, `gpt-3.5-turbo`.",
)
@click.option(
    "-st",
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
@click.option(
    "-w",
    "--overwrite",
    is_flag=True,
    default=False,
    show_default=True,
    help="If `True`, it will directly write the docstrings into the files (it will not generate git patches)",
)
@click.option(
    "-p",
    "--ignore-private",
    is_flag=True,
    default=False,
    show_default=False,
    help=(
        "Ignore private classes, methods, and functions starting with two "
        "underscores.  [default: False]"
    ),
)
@click.option(
    "-s",
    "--ignore-semiprivate",
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        "Ignore semiprivate classes, methods, and functions starting with a "
        "single underscore."
    ),
)
@click.option(
    "-i",
    "--ignore-init-method",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore `__init__` method of classes.",
)
@click.option(
    "-C",
    "--ignore-nested-classes",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore nested classes.",
)
@click.option(
    "-n",
    "--ignore-nested-functions",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore nested functions and methods.",
)
@click.option(
    "-P",
    "--ignore-property-decorators",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore methods with property setter/getter decorators.",
)
@click.option(
    "-S",
    "--ignore-setters",
    is_flag=True,
    default=False,
    show_default=True,
    help="Ignore methods with property setter decorators.",
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

    config = GPT4DocstringsConfig(
        overwrite=kwargs["overwrite"],
        ignore_private=kwargs["ignore_private"],
        ignore_semiprivate=kwargs["ignore_semiprivate"],
        ignore_init_method=kwargs["ignore_init_method"],
        ignore_nested_classes=kwargs["ignore_nested_classes"],
        ignore_nested_functions=kwargs["ignore_nested_functions"],
        ignore_property_setters=kwargs["ignore_setters"],
        ignore_property_decorators=kwargs["ignore_property_decorators"],
    )

    docstrings_generator = gpt4docstrings.GPT4Docstrings(
        paths=paths,
        excluded=kwargs["exclude"],
        model=kwargs["model"],
        docstring_style=kwargs["style"],
        api_key=kwargs["api_key"],
        verbose=kwargs["verbose"],
        config=config,
    )
    docstrings_generator.generate_docstrings()
