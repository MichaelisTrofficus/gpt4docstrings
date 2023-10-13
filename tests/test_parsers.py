import pytest

from gpt4docstrings.docstrings_generators.utils.parsers import DocstringParser
from gpt4docstrings.docstrings_generators.utils.parsers import DocstringParsingError


def test_function_docstring():
    parser = DocstringParser()
    text = "```This is a function docstring```"
    result = parser.parse(text)
    assert result == "This is a function docstring"


def test_empty_function_docstring():
    parser = DocstringParser()
    text = "``` ```"
    result = parser.parse(text)
    assert result == ""


def test_function_missing_backticks():
    parser = DocstringParser()
    text = "This is not a function docstring"
    with pytest.raises(DocstringParsingError):
        parser.parse(text)


def test_valid_class_docstring():
    parser = DocstringParser()
    text = (
        '```class MyClass:\n """This is a class docstring"""\n def method1(self):\n   '
        ' """Method 1 docstring"""\n  def method2(self):\n    """Method 2 docstring"""\n```'
    )
    result = parser.parse(text)
    expected_result = (
        'class MyClass:\n """This is a class docstring"""\n def method1(self):\n '
        '   """Method 1 docstring"""\n  def method2(self):\n    """Method 2 docstring"""'
    )
    assert result == expected_result


def test_empty_class_docstring():
    parser = DocstringParser()
    text = (
        '```class MyClass:\n """ """\n  def method1(self):\n    """Method 1 docstring"""\n  '
        'def method2(self):\n    """Method 2 docstring"""\n```'
    )
    result = parser.parse(text)
    expected_result = (
        'class MyClass:\n """ """\n  def method1(self):\n    """Method 1 docstring"""\n  '
        'def method2(self):\n    """Method 2 docstring"""'
    )
    assert result == expected_result


def test_class_missing_backticks():
    parser = DocstringParser()
    text = "This is not a class docstring"
    with pytest.raises(DocstringParsingError):
        parser.parse(text)
