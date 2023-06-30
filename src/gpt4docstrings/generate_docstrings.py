import os
import pathlib
import sys
from fnmatch import fnmatch
from typing import List
from typing import Union

from redbaron import RedBaron

from gpt4docstrings import utils
from gpt4docstrings.docstrings_generators import ChatGPTDocstringGenerator


class GPT4Docstrings:
    def __init__(
        self,
        paths: Union[str, List[str]],
        excluded=None,
        model: str = "gpt-3.5-turbo",
        docstrings_style: str = "google",
        api_key: str = None,
    ):
        self.paths = paths
        self.excluded = excluded or ()
        self.common_base = pathlib.Path("/")
        self.docstring_generator = ChatGPTDocstringGenerator(
            api_key=api_key, model=model, docstrings_style=docstrings_style
        )

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

        for node in source.find_all("def"):
            if not node.value[
                0
            ].type == "string" and not utils.check_def_node_is_class_method(node):
                docstring_dict = self.docstring_generator.generate_function_docstring(
                    node.dumps()
                )
                node.value.insert(0, docstring_dict["docstring"])

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

        utils.write_updated_source_to_file(source, filename)

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
        self._generate_docstrings(filenames)
