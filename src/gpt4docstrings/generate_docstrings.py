import ast
import asyncio
import os
import pathlib
import sys
from fnmatch import fnmatch
from typing import List
from typing import Union

import click
from colorama import Fore
from tabulate import tabulate

from gpt4docstrings import utils
from gpt4docstrings.ascii_title import title
from gpt4docstrings.config import GPT4DocstringsConfig
from gpt4docstrings.docstrings_generators import ChatGPTDocstringGenerator
from gpt4docstrings.visit import GPT4DocstringsVisitor


class GPT4Docstrings:
    """A class for generating docstrings for Python files using GPT-4 model.

    Args:
        paths (Union[str, List[str]]): The paths to the Python files or directories to generate docstrings for.
        excluded (Optional): A list of file patterns to exclude from docstring generation. Defaults to None.
        model (str): The GPT model to use for generating docstrings. Defaults to "gpt-3.5-turbo".
        docstring_style (str): The style of docstrings to generate. Must be one of ["google", "numpy",
            "reStructuredText", "epytext"]. Defaults to "google".
        api_key (str): The API key for accessing the GPT model. Defaults to None.
        verbose (int): The verbosity level. Set to 0 for no output, 1 for basic output, and 2 for detailed output.
            Defaults to 0.
        config (GPT4DocstringsConfig): Configuration for GPT4Docstrings


    Attributes:
        paths (Union[str, List[str]]): The paths to the Python files or directories to generate docstrings for.
        excluded (Optional): A list of file patterns to exclude from docstring generation.
        common_base (pathlib.Path): The common base path of the input files or directories.
        docstring_generator (ChatGPTDocstringGenerator): The docstring generator object.
        verbose (int): The verbosity level.
        documented_nodes (List[List[str]]): A list of documented functions and classes.

    Methods:
        print_pretty_documentation_table: Prints a pretty table of the documented functions and classes.
        _filter_files: Filters the input files based on the excluded patterns.
        get_filenames_from_paths: Retrieves the filenames from the input paths.
        _generate_file_docstrings: Generates docstrings for a single file.
        _generate_docstrings: Generates docstrings for multiple files.
        generate_docstrings: Generates docstrings for the input files or directories.
    """

    def __init__(
        self,
        paths: Union[str, List[str]],
        excluded=None,
        model: str = "gpt-3.5-turbo",
        docstring_style: str = "google",
        api_key: str = None,
        verbose: int = 0,
        config: GPT4DocstringsConfig = None,
    ):
        self.paths = paths
        self.excluded = excluded or ()
        self.common_base = pathlib.Path("/")

        if docstring_style not in ["google", "numpy", "reStructuredText", "epytext"]:
            raise ValueError(
                "Docstring Style must be one of the following: "
                '["google", "numpy", "reStructuredText", "epytext"]'
            )
        self.docstring_generator = ChatGPTDocstringGenerator(
            api_key=api_key, model_name=model, docstring_style=docstring_style
        )

        self.verbose = verbose
        self.documented_nodes = []
        self.config = config

    def __print_pretty_documentation_table(self):
        """Prints a pretty table of the documented functions and classes."""
        headers = ["Filename", "Documented Functions / Classes"]
        table = [x for x in self.documented_nodes]
        print(Fore.GREEN + tabulate(table, headers, tablefmt="outline"))

    def __filter_files(self, files: List[str]):
        """Filters the input files based on the excluded patterns.

        Args:
            files (List[str]): The list of file paths to filter.

        Yields:
            str: The filtered file paths.
        """
        for f in files:
            if not f.endswith(".py"):
                continue

            # By default, we will ignore __init__.py files
            basename = os.path.basename(f)
            if basename == "__init__.py":
                continue

            if any(fnmatch(f, exc + "*") for exc in self.excluded):
                continue
            yield f

    def get_filenames_from_paths(self) -> List[str]:
        """Retrieves the filenames from the input paths.

        Returns:
            List[str]: The list of filenames.
        """
        filenames = []

        for path in self.paths:
            if os.path.isfile(path):
                if not path.endswith(".py"):
                    return sys.exit(1)

                if not any(fnmatch(path, exc + "*") for exc in self.excluded):
                    filenames.append(path)

                continue

            for root, _, fs in os.walk(path):
                full_paths = [os.path.join(root, f) for f in fs]
                filenames.extend(self.__filter_files(full_paths))

        if not filenames:
            return sys.exit(1)

        self.common_base = utils.get_common_base(filenames)
        return filenames

    @staticmethod
    def _filter_nodes(nodes):
        """Filters the parsed nodes to only consider classes and functions"""
        return [
            node
            for node in nodes
            if (
                (node.node_type in ["ClassDef", "FunctionDef", "AsyncFunctionDef"])
                and not node.covered
            )
        ]

    @staticmethod
    def _filter_inner_nested(nodes):
        """Filters out children of ignored nested funcs / classes."""
        nested_cls = [n for n in nodes if n.is_nested_cls]
        inner_nested_nodes = [n for n in nodes if n.parent in nested_cls]

        filtered_nodes = [n for n in nodes if n not in inner_nested_nodes]
        filtered_nodes = [n for n in filtered_nodes if n not in nested_cls]
        return filtered_nodes

    async def generate_file_docstrings(self, filename: str):
        """
        Generates docstrings for a single file.

        Args:
            filename (str): The path of the file to generate docstrings for.
        """
        click.echo(click.style(f"Documenting file {filename} ... ", fg="green"))

        with open(filename, encoding="utf-8") as f:
            source_tree = f.read()

        parsed_tree = ast.parse(source_tree)
        visitor = GPT4DocstringsVisitor(
            filename=filename, config=GPT4DocstringsConfig()
        )
        visitor.visit(parsed_tree)
        nodes = self._filter_nodes(visitor.nodes)
        tasks = []

        for node in nodes:
            tasks.append(self.docstring_generator.generate_docstring(node))
            self.documented_nodes.append([filename, node.name])

        docstrings = await asyncio.gather(*tasks)
        for node, docstring in zip(nodes, docstrings, strict=True):
            node.ast_node.body.insert(0, docstring.to_ast())

        self._write_to_filename(filename, ast.unparse(parsed_tree))

    @staticmethod
    def _write_to_filename(filename: str, content: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_docstrings(self):
        """Generates docstrings for the input files or directories."""
        filenames = self.get_filenames_from_paths()
        click.echo(click.style(title, fg="green"))
        loop = asyncio.get_event_loop()

        for filename in filenames:
            loop.run_until_complete(self.generate_file_docstrings(filename))

        if self.verbose > 0:
            self.__print_pretty_documentation_table()
