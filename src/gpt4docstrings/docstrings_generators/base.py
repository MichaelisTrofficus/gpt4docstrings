import abc


class DocstringGenerator(abc.ABC):
    """
    An abstract base class for docstring generators that provides a blueprint for generating
    docstrings for functions and classes.

    Methods:
        generate_docstring(source: str) -> dict:
            Generate a docstring for the provided source code.
    """

    @abc.abstractmethod
    def generate_docstring(self, source: str) -> dict:
        raise NotImplementedError(
            "Method `generate_function_docstring` is not implemented."
        )
