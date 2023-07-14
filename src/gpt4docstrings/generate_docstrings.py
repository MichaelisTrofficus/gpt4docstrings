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


class GPT4Docstrings:
    def __init__(
        self,
        paths: Union[str, List[str]],
        excluded=None,
        model: str = "gpt-3.5-turbo",
        api_key: str = None,
        verbose: int = 0,
    ):
        self.paths = paths
        self.excluded = excluded or ()
        self.common_base = pathlib.Path("/")
        self.docstring_generator = ChatGPTDocstringGenerator(
            api_key=api_key, model=model
        )
        self.verbose = verbose
        self.documented_nodes = []

    def print_pretty_documentation_table(self):
        """
        Prints a pretty table to terminal when verbose is greater than zero. The table contains
        one row per each node (function or class) examined by `gpt4docstrings`. One of the columns
        refers to the node name and the other one shows if the node has been documented.
        """
        headers = ["Filename", "Documented Functions / Classes"]
        table = [x for x in self.documented_nodes]
        print(Fore.GREEN + tabulate(table, headers, tablefmt="outline"))

    def _filter_files(self, files: List[str]):
        """
        Filter files that are explicitly excluded

        Args:
            files: A list of files to be filtered

        Yields:
            Files which are not filtered
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
        """
        Find all python files inside `paths` provided by the user

        Returns:
            A list of file names
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
                filenames.extend(self._filter_files(full_paths))

        if not filenames:
            return sys.exit(1)

        self.common_base = utils.get_common_base(filenames)
        return filenames

    def _generate_file_docstrings(self, filename: str):
        """
        Generates docstrings for a file.

        Args:
            filename: The filename to be potentially documented
        """
        source = RedBaron(open(filename, encoding="utf-8").read())
        click.echo(click.style(f"* Documenting file {filename} ... \n", fg="green"))

        for node in source.find_all("def"):
            if not utils.check_def_node_is_class_method(node):
                if not node.value[0].type == "string":
                    docstring_dict = (
                        self.docstring_generator.generate_function_docstring(
                            node.dumps()
                        )
                    )
                    node.value.insert(0, docstring_dict["docstring"])
                    self.documented_nodes.append([filename, node.name])

        for node in source.find_all("class"):
            if not node.value[0].type == "string":
                docstring_dict = self.docstring_generator.generate_class_docstring(
                    node.dumps()
                )
                node.value.insert(0, docstring_dict["docstring"])

                for method_node in node.value:
                    if (
                        method_node.type == "def"
                        and not utils.check_is_private_method(method_node)
                        and not method_node.value[0].type == "string"
                    ):
                        method_node.value.insert(0, docstring_dict[method_node.name])

                self.documented_nodes.append([filename, node.name])

        utils.write_updated_source_to_file(source, filename)
        os.system(f"docformatter --in-place {filename}")

        if self.verbose > 0:
            self.print_pretty_documentation_table()

    def _generate_docstrings(self, filenames: List[str]):
        """
        Traverses the filenames and generate docstrings for undocumented classes / functions
        inside each file.

        Args:
            filenames: A list of files to be potentially documented.
        """
        for filename in filenames:
            self._generate_file_docstrings(filename)

    def generate_docstrings(self):
        """Generates docstrings for undocumented classes / functions"""
        filenames = self.get_filenames_from_paths()

        click.echo(click.style(title, fg="green"))
        self._generate_docstrings(filenames)
