import abc


class DocstringTranslator(abc.ABC):
    """
    An abstract base class for docstring translators that provides a blueprint for translating
    docstrings for functions and classes.

    Methods:
        translate_docstring(source: str) -> dict:
            Translate a docstring based on the provided source code.
    """

    @abc.abstractmethod
    def translate_docstring(self, source: str) -> dict:
        raise NotImplementedError(
            "Method `generate_function_docstring` is not implemented."
        )
