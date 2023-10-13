import pytest

from gpt4docstrings.docstrings_generators.utils.parsers import ClassDocstringParser
from gpt4docstrings.docstrings_generators.utils.parsers import DocstringParsingError
from gpt4docstrings.docstrings_generators.utils.parsers import FunctionDocstringParser


def test_function_docstring():
    parser = FunctionDocstringParser()
    text = "```This is a function docstring```"
    result = parser.parse(text)
    assert result == "This is a function docstring"


def test_empty_function_docstring():
    parser = FunctionDocstringParser()
    text = "``` ```"
    result = parser.parse(text)
    assert result == ""


def test_function_missing_backticks():
    parser = FunctionDocstringParser()
    text = "This is not a function docstring"
    with pytest.raises(DocstringParsingError):
        parser.parse(text)


def test_valid_class_docstring():
    parser = ClassDocstringParser()
    text = (
        '```class MyClass:\n """This is a class docstring"""\n def method1(self):\n   '
        ' """Method 1 docstring"""\n  def method2(self):\n    """Method 2 docstring"""\n```'
    )
    result = parser.parse(text)
    result = {key: value.dumps() for key, value in result.items()}
    expected_result = {
        "docstring": '"""This is a class docstring"""',
        "method1": '"""Method 1 docstring"""',
        "method2": '"""Method 2 docstring"""',
    }
    assert result == expected_result


def test_empty_class_docstring():
    parser = ClassDocstringParser()
    text = (
        '```class MyClass:\n """ """\n  def method1(self):\n    """Method 1 docstring"""\n  '
        'def method2(self):\n    """Method 2 docstring"""\n```'
    )
    result = parser.parse(text)
    result = {key: value.dumps() for key, value in result.items()}
    expected_result = {
        "docstring": '""" """',
        "method1": '"""Method 1 docstring"""',
        "method2": '"""Method 2 docstring"""',
    }
    assert result == expected_result


def test_class_missing_backticks():
    parser = ClassDocstringParser()
    text = "This is not a class docstring"
    with pytest.raises(DocstringParsingError):
        parser.parse(text)
