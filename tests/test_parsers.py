import pytest

from gpt4docstrings.utils.parsers import DocstringParser
from gpt4docstrings.utils.parsers import DocstringParsingError


def test_docstring():
    parser = DocstringParser()
    text = '"""\nThis is a function docstring"""'
    result = parser.parse(text)
    assert result == "This is a function docstring"


def test_empty_docstring():
    parser = DocstringParser()
    text = '""""""'
    result = parser.parse(text)
    assert result == ""


def test_missing_backticks():
    parser = DocstringParser()
    text = "This is not a function docstring"
    with pytest.raises(DocstringParsingError):
        parser.parse(text)
