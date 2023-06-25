import os
import pathlib
import sys
from fnmatch import fnmatch
from typing import List
from typing import Union

from redbaron import RedBaron

from gpt4docstrings import utils


class GPT4Docstrings:
    def __init__(self, paths: Union[str, List[str]], excluded=None):
        self.paths = paths
        self.excluded = excluded or ()
        self.common_base = pathlib.Path("/")
        self.excluded_special_methods = [
            "__new__",
            "__init__",
            "__del__",
            "__repr__",
            "__str__",
            "__cmp__",
            "__hash__",
            "__nonzero__",
            "__unicode__",
            "__getattribute__",
            "__getattr__",
            "__setattr__",
            "__delattr__",
            "__get__",
            "__set__",
            "__delete__",
            "__len__",
            "__getitem__",
            "__setitem__",
            "__delitem__",
            "__getslice__",
            "__setslice__",
            "__delslice__",
            "__contains__",
            "__add__",
            "__sub__",
            "__mul__",
            "__div__",
            "__truediv__",
            "__floordiv__",
            "__mod__",
            "__divmod__",
            "__pow__",
            "__lshift__",
            "__rshift__",
            "__and__",
            "__or__",
            "__xor__",
            "__radd__",
            "__rsub__",
            "__rmul__",
            "__rdiv__",
            "__rtruediv__",
            "__rfloordiv__",
            "__rmod__",
            "__rdivmod__",
            "__rpow__",
            "__rlshift__",
            "__rrshift__",
        ]

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
        docstring = "This is a generated docstring!!"

        for node in source.find_all("def"):
            if not node.value[
                0
            ].type == "string" and not utils.check_def_node_is_class_method(node):
                node.value.insert(0, f'"""\n{docstring}\n"""')

        for node in source.find_all("class"):
            if not node.value[0].type == "string":
                node.value.insert(0, f'"""\n{docstring}\n"""')

            for method_node in node.value:
                if (
                    method_node.type == "def"
                    and method_node.name not in self.excluded_special_methods
                    and not method_node.value[0].type == "string"
                ):
                    method_node.value.insert(0, f'"""\n\t{docstring}\n\t"""')

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
