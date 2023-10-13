import re

from langchain.schema import BaseOutputParser
from redbaron import RedBaron


class DocstringParsingError(Exception):
    """Custom exception for docstring parsing errors."""

    pass


class DocstringParsersBase(BaseOutputParser):
    def parse(self, text: str):
        pattern = r"```(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise DocstringParsingError(
                "Something went wrong when parsing the exception"
            )


class FunctionDocstringParser(DocstringParsersBase):
    def parse(self, text: str):
        return super().parse(text)


class ClassDocstringParser(DocstringParsersBase):
    def parse(self, text: str):
        class_str = super().parse(text)
        class_node = RedBaron(class_str)[0]
        method_nodes = [f for f in class_node.find_all("def")]

        docstrings = {}
        for method_node in method_nodes:
            docstrings[method_node.name] = method_node.value[0]

        docstrings["docstring"] = class_node.value[0]
        return docstrings
