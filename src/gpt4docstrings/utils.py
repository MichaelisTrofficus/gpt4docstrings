import os
import pathlib
import re
import textwrap
from typing import List

from redbaron import Node
from redbaron import RedBaron


def get_common_base(files: List[str]) -> str:
    """Returns the common base directory path for a list of files.

    Args:
        files (List[str]): A list of file paths.

    Returns:
        str: The common base directory path.

    Example:
        files = ['/path/to/file1.txt', '/path/to/file2.txt', '/path/to/file3.txt']
        get_common_base(files)
        '/path/to'
    """
    common_base = pathlib.Path(os.path.commonprefix(files))
    while not common_base.exists():
        common_base = common_base.parent
    return str(common_base)


def check_def_node_is_nested(node) -> bool:
    """Check if the given node is a nested function.

    Args:
        node: The node to check

    Returns:
        bool: True if the node is a nested function, False otherwise.
    """
    try:
        is_nested = True if node.parent.type == "def" else False
    except AttributeError:
        is_nested = False
    return is_nested


def check_def_node_is_class_method(node) -> bool:
    """Check if the given node is a class method.

    Args:
        node: The node to check.

    Returns:
        bool: True if the node is a class method, False otherwise.
    """
    try:
        is_method = True if node.parent.type == "class" else False
    except AttributeError:
        is_method = False
    return is_method


def write_updated_source_to_file(source: RedBaron, filename: str):
    """
    Writes the updated source code to a file.

    Args:
        source (RedBaron): The updated source code represented as a RedBaron object.
        filename (str): The name of the file to write the source code to.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(source.dumps())


def check_is_private_method(node: Node) -> bool:
    """Checks if a given node is a private method.

    Args:
        node (Node): The node to check.

    Returns:
        bool: True if the node is a private method, False otherwise.
    """
    return all(
        [
            node.name.startswith("__"),
            node.name.endswith("__"),
        ]
    )


def match_between_characters(string: str, start_char: str, end_char: str):
    """Extracts the substring between two specified characters in a given string.

    Args:
        string (str): The input string from which the substring will be extracted.
        start_char (str): The starting character of the substring.
        end_char (str): The ending character of the substring.

    Returns:
        str or None: The substring between the start_char and end_char if found, otherwise None.

    Example:
        match_between_characters("Hello [world]!", "[", "]")
        'world'
    """
    pattern = re.escape(start_char) + "(.*?)" + re.escape(end_char)
    match = re.search(pattern, string, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def add_indentation_to_docstring(text: str, indentation: str):
    """
    Add a specified level of indentation to a given multiline string.

    Args:
        text (str): The multiline string to which indentation will be added.
        indentation (str): The indentation represented by an empty string. The length
            of this string is the same as the indentation level

    Returns:
        str: The multiline string with the specified indentation level added.
    """
    return textwrap.indent(text, indentation)
