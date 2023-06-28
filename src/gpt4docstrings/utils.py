import os
import pathlib
from typing import List

from redbaron import Node
from redbaron import RedBaron


def get_common_base(files: List[str]) -> str:
    """
    Finds the common parent base for a list of files.

    Args:
        files: A list of files

    Returns:
        Common base path
    """
    common_base = pathlib.Path(os.path.commonprefix(files))
    while not common_base.exists():
        common_base = common_base.parent
    return str(common_base)


def check_def_node_is_class_method(node) -> bool:
    """
    Checks if the given DefNode is a class method

    Args:
        node: A DefNode

    Returns:
        `True` if the DefNode is indeed a Class Method. False otherwise.
    """
    try:
        is_method = True if node.parent.type == "class" else False
    except AttributeError:
        is_method = False
    return is_method


def write_updated_source_to_file(source: RedBaron, filename: str):
    """
    Runs RedBaron updated source code to file.

    Args:
        source: A RedBaron object representing the updated source code
        filename: The filename where updated code will be written.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(source.dumps())


def check_is_private_method(node: Node) -> bool:
    """
    Check if current node is a private method in a class.

    Args:
        node: A RedBaron node

    Returns:
        `True` if the method is private, `False` otherwise
    """
    return all(
        [
            node.name.startswith("__"),
            node.name.endswith("__"),
        ]
    )
