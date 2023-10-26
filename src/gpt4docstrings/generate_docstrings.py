import ast
import asyncio
import difflib
import os
import pathlib
import sys
from fnmatch import fnmatch
from typing import List
from typing import Union

import click
from colorama import Fore
from tabulate import tabulate
from tqdm.asyncio import tqdm_asyncio

from gpt4docstrings import utils
from gpt4docstrings.ascii_title import title
from gpt4docstrings.config import GPT4DocstringsConfig
from gpt4docstrings.docstrings_generators import ChatGPTDocstringGenerator
from gpt4docstrings.docstrings_generators.docstring import Docstring
from gpt4docstrings.visit import GPT4DocstringsVisitor


class GPT4Docstrings:
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

        self.patches = []

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
            if path.startswith("./"):
                path = path[2:]

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

    @staticmethod
    def _read_file(filename: str, read_lines: bool = False) -> Union[str, List[str]]:
        with open(filename, encoding="utf-8") as file:
            return file.readlines() if read_lines else file.read()

    @staticmethod
    def _write_to_file(filename: str, content: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _build_file_with_docstrings(source_file: str, docstrings: List[Docstring]):
        docstrings_positions = {
            docstring.lineno - 1: docstring.to_str() for docstring in docstrings
        }

        lines = []

        for i, line in enumerate(source_file.split("\n")):
            lines.append(line)
            if i in docstrings_positions:
                lines.extend(docstrings_positions[i].splitlines())

        target_file = "\n".join(lines)

        return target_file

    @staticmethod
    def _get_patch_lines(src: str, target: str, filename: str):
        src_lines = [line + "\n" for line in src.splitlines()]
        target_lines = [line + "\n" for line in target.splitlines()]

        fromfile = "a/" + filename
        tofile = "b/" + filename

        differ = list(
            difflib.unified_diff(
                src_lines, target_lines, fromfile=fromfile, tofile=tofile
            )
        )
        return differ

    def _generate_patch_file(self, src: str, target: str, filename: str):
        differ = self._get_patch_lines(src, target, filename)
        self.patches.append(differ)

    def _write_concatenated_patch_file(self):
        concatenated_patch = []

        for patch in self.patches:
            concatenated_patch.extend(patch)
            concatenated_patch.append("\n")

        if concatenated_patch:
            with open(
                "gpt4docstring_docstring_generator_patch.diff", "w"
            ) as patch_file:
                patch_file.writelines(concatenated_patch)

    async def generate_file_docstrings(self, filename: str):
        """
        Generates docstrings for a single file.

        Args:
            filename (str): The path of the file to generate docstrings for.
        """
        click.echo(f"\n\n Documenting filename {filename} ... ")
        with open(filename, encoding="utf-8") as f:
            source_file = f.read()

        parsed_tree = ast.parse(source_file)
        visitor = GPT4DocstringsVisitor(
            filename=filename, config=GPT4DocstringsConfig()
        )
        visitor.visit(parsed_tree)
        nodes = self._filter_inner_nested(self._filter_nodes(visitor.nodes))

        tasks = []

        for node in nodes:
            tasks.append(self.docstring_generator.generate_docstring(node))
            self.documented_nodes.append([filename, node.name])

        docstrings = await tqdm_asyncio.gather(*tasks)
        target_file = self._build_file_with_docstrings(source_file, docstrings)

        if self.config.overwrite:
            self._write_to_file(filename, target_file)
        else:
            self._generate_patch_file(source_file, target_file, filename)

    def generate_docstrings(self):
        """Generates docstrings for the input files or directories."""
        filenames = self.get_filenames_from_paths()
        click.echo(click.style(title, fg="green"))
        loop = asyncio.get_event_loop()

        for filename in filenames:
            loop.run_until_complete(self.generate_file_docstrings(filename))

        if not self.config.overwrite:
            self._write_concatenated_patch_file()

        if self.verbose > 0:
            self.__print_pretty_documentation_table()
