import re

from langchain.schema import BaseOutputParser


class DocstringParsingError(Exception):
    """Custom exception for docstring parsing errors."""

    pass


class DocstringParser(BaseOutputParser):
    def parse(self, text: str):
        pattern = r"```(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise DocstringParsingError("Something went wrong when parsing")
