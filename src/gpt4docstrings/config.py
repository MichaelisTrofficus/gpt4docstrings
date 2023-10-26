# Copyright 2020 Lynn Root
"""Configuration-related helpers."""
# Adapted from Black https://github.com/psf/black/blob/master/black.py.
# This code is adapted from Lynn Root's interrogate library: https://github.com/econchick/interrogate
import pathlib

import attr


# TODO: idea: break out InterrogateConfig into two classes: one for
# running the tool, one for reporting the results
@attr.s
class GPT4DocstringsConfig:
    """
    Configuration related to interrogating a given codebase.

    Args:
        overwrite (bool): If `True`, the documented file will be overwritten. This may be dangerous
            in same cases, so it's better to use patches to confirm the changes to be applied.
        ignore_private (bool): Ignore private classes, methods, and
            functions starting with two underscores.
        ignore_semiprivate (bool): Ignore semiprivate classes, methods,
            and functions starting with a single underscore.
        ignore_init_method (bool): Ignore ``__init__`` method of
            classes.
        ignore_nested_functions (bool): Ignore nested functions and
            methods.
    """

    overwrite = attr.ib(default=False)
    ignore_private = attr.ib(default=False)
    ignore_semiprivate = attr.ib(default=False)
    ignore_init_method = attr.ib(default=False)
    ignore_nested_classes = attr.ib(default=False)
    ignore_nested_functions = attr.ib(default=False)
    ignore_property_setters = attr.ib(default=False)
    ignore_property_decorators = attr.ib(default=False)


def find_project_root(srcs):
    """
    Return a directory containing .git, .hg, or pyproject.toml.
    That directory can be one of the directories passed in `srcs` or their
    common parent.
    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.k
    """
    if not srcs:
        return pathlib.Path("/").resolve()

    common_base = min(pathlib.Path(src).resolve() for src in srcs)
    if common_base.is_dir():
        # Append a fake file so `parents` below returns `common_base_dir`, too.
        common_base /= "fake-file"

    for directory in common_base.parents:
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory
