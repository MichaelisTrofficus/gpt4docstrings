import os
import pathlib
from typing import List


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
