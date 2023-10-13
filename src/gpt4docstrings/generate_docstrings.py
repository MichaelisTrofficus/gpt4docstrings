import logging
import os
import pathlib
import sys
from fnmatch import fnmatch
from typing import List
from typing import Union

import click
from colorama import Fore
from redbaron import RedBaron
from tabulate import tabulate

from gpt4docstrings import utils
from gpt4docstrings.ascii_title import title
from gpt4docstrings.docstrings_generators import ChatGPTDocstringGenerator
from gpt4docstrings.exceptions import ASTError
from gpt4docstrings.exceptions import DocstringParsingError


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

    # flake8: noqa: C901
    def generate_file_docstrings(self, filename: str):
        """Generates docstrings for a single file.

        Args:
            filename (str): The path of the file to generate docstrings for.
        """
        source = RedBaron(open(filename, encoding="utf-8").read())
        click.echo(click.style(f"Documenting file {filename} ... ", fg="green"))

        for node in source.find_all("def"):
            if not utils.check_def_node_is_class_method(
                node
            ) and not utils.check_def_node_is_nested(node):
                if not node.value[0].type == "string":
                    try:
                        fn_docstring = (
                            self.docstring_generator.generate_function_docstring(
                                node.dumps()
                            )
                        )
                        node.value.insert(0, fn_docstring["docstring"])
                        self.documented_nodes.append([filename, node.name])
                    except DocstringParsingError:
                        logging.warning(
                            f"Skipping {node.name} from {filename} due to errors when parsing"
                        )
                    except ASTError:
                        logging.warning(
                            f"Skipping {node.name} from {filename} due to errors when accessing AST node"
                        )

        for node in source.find_all("class"):
            if not node.value[0].type == "string":
                try:
                    class_docstring = self.docstring_generator.generate_class_docstring(
                        node.dumps()
                    )
                    node.value.insert(
                        0,
                        class_docstring["docstring"],
                    )

                    for method_node in node.value:
                        if (
                            method_node.type == "def"
                            and not utils.check_is_private_method(method_node)
                            and not method_node.value[0].type == "string"
                            and not utils.check_def_node_is_nested(method_node)
                        ):
                            method_node.value.insert(
                                0, class_docstring[method_node.name]
                            )

                    self.documented_nodes.append([filename, node.name])
                except DocstringParsingError:
                    logging.warning(
                        f"Skipping {node.name} from {filename} due to errors when parsing"
                    )
                except ASTError:
                    logging.warning(
                        f"Skipping {node.name} from {filename} due to errors when accessing AST node"
                    )

        utils.write_updated_source_to_file(source, filename)

    def generate_docstrings(self):
        """Generates docstrings for the input files or directories."""
        filenames = self.get_filenames_from_paths()
        click.echo(click.style(title, fg="green"))

        for filename in filenames:
            self.generate_file_docstrings(filename)

        if self.verbose > 0:
            self.__print_pretty_documentation_table()
