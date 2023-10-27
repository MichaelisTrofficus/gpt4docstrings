import ast
import textwrap


class Docstring:
    """
    A class representing a docstring.

    Attributes:
        text (str): The text of the docstring.
        col_offset (int): The column offset of the docstring.
        lineno (int): The line number of the docstring.
        indentation (str): The indentation string used for the docstring.
    """

    def __init__(self, text: str, col_offset: int, lineno: int):
        """
        Initialize an instance of a class.

        Args:
            text (str): The text value to assign to the instance's `text` attribute.
            col_offset (int): The column offset value to assign to the instance's `col_offset` attribute.
            lineno (int): The line number value to assign to the instance's `lineno` attribute.
        """
        self.text = text
        self.col_offset = col_offset
        self.lineno = lineno
        self.indentation = " " * col_offset

    def to_ast(self):
        """
        Gets the docstring as an ast.Expr node.

        Returns:
            ast.Expr: The AST node representing the docstring.
        """
        return ast.Expr(
            ast.Constant(
                "\n"
                + textwrap.indent(self.text + "\n" + self.indentation, self.indentation)
            )
        )

    def to_str(self, add_triple_quotes: bool = True):
        """
        Returns a string representation of the docstring, with indentation.

        Args:
            add_triple_quotes (bool): If `True`, return the plain text indented, without the triple quotes.

        Returns:
            str: The string representation of the docstring, with indentation applied.
        """
        self.text = "\n" + self.text + "\n"

        if add_triple_quotes:
            self.text = '"""' + self.text + '"""'

        return textwrap.indent(self.text + self.indentation, self.indentation)
