import ast
import textwrap


class Docstring:
    def __init__(self, text: str, col_offset: int):
        self.text = text
        self.col_offset = col_offset
        self.indentation = " " * col_offset

    def to_ast(self):
        return ast.Expr(
            ast.Constant(
                "\n"
                + textwrap.indent(self.text + "\n" + self.indentation, self.indentation)
            )
        )
