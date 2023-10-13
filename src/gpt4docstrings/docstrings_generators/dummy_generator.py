from gpt4docstrings.docstrings_generators.base import DocstringGenerator


class DummyDocstringGenerator(DocstringGenerator):
    """Dummy example for creating a Docstring Generator."""

    def __init__(
        self,
    ):
        self.function_docstring = "This is a function docstring"
        self.class_docstring = "This is a class docstring"

    def generate_function_docstring(self, source: str) -> dict:
        return {"docstring": self.function_docstring}

    def generate_class_docstring(self, source: str) -> dict:
        return {"docstring": self.class_docstring}
