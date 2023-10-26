import abc


class DocstringGenerator(abc.ABC):
    """
    An abstract base class for docstring generators that provides a blueprint for generating
    docstrings for functions and classes.

    Methods:
        generate_function_docstring(source: str) -> dict:
            Generate a docstring for a function based on the provided source code.

        generate_class_docstring(source: str) -> dict:
            Generate a docstring for a class based on the provided source code.

    Abstract Methods:
        These methods must be implemented by subclasses:
        - generate_function_docstring(source: str) -> dict
        - generate_class_docstring(source: str) -> dict

    Note:
        Subclasses of DocstringGenerator must implement the abstract methods to provide
        specific docstring generation functionality.

    Example Usage:
        To use this abstract class, create a concrete subclass that implements the
        'generate_function_docstring' and 'generate_class_docstring' methods.
    """

    @abc.abstractmethod
    def generate_docstring(self, source: str) -> dict:
        raise NotImplementedError(
            "Method `generate_function_docstring` is not implemented."
        )
