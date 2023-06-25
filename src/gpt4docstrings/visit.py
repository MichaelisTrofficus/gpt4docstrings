# Copyright 2020 Lynn Root

import ast
import os
import sys

import attr


PY_38_HIGHER = sys.version_info >= (3, 8)


@attr.s(eq=False)
class DocsNode:
    """
    Docstrings AST Node.
    """
    name = attr.ib()
    path = attr.ib()
    level = attr.ib()
    lineno = attr.ib()
    end_lineno = attr.ib()
    covered = attr.ib()
    source_code = attr.ib()
    node_type = attr.ib()
    is_nested_func = attr.ib()
    is_nested_cls = attr.ib()
    parent = attr.ib()


class DocstringWriter(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        docstring = ast.get_docstring(node)
        new_docstring_node = make_docstring_node(docstring)

        with open("../pruebas.py") as f:
            lines = f.readlines()

        with open("../pruebas.py", "w") as f:
            lines.insert(node.lineno + 1, "Hola mundo")
            f.write("\n".join(lines))

        if docstring:
            # Assumes the existing docstring is the first node
            # in the function body.
            node.body[0] = new_docstring_node
        else:
            node.body.insert(0, new_docstring_node)
        return node


def make_docstring_node(docstring):
    if docstring is None:
        content = "A new docstring"
    else:
        content = docstring + " -- amended"
    s = ast.Str(content)
    return ast.Expr(value=s)


class DocsTransformer(ast.NodeTransformer):
    """NodeVisitor for a Python file to find docstrings.

    :param str filename: filename to parse coverage.
    :param config.InterrogateConfig config: configuration.
    """

    def __init__(self, filename, source, config):
        self.filename = filename
        self.source = source
        self.stack = []
        self.nodes = []
        self.config = config

    @staticmethod
    def _has_doc(node):
        """Return if node has docstrings."""
        return (
            ast.get_docstring(node) is not None
            and ast.get_docstring(node).strip() != ""
        )

    @staticmethod
    def _get_source_code(source, node):
        return ast.get_source_segment(source, node)

    @staticmethod
    def _make_docstring_node(source: str):
        """
        This method will call ChatGPT or whatever LLM model
        Args:
            source: The source code
        """
        source = "Hi, this is our first docstring"
        s = ast.Str(source)
        return ast.Expr(value=s)

    def _visit_helper(self, node):
        """Recursively visit AST node for docstrings."""
        if not hasattr(node, "name"):
            node_name = os.path.basename(self.filename)
        else:
            node_name = node.name

        parent = None
        path = node_name

        if self.stack:
            parent = self.stack[-1]
            parent_path = parent.path
            if parent_path.endswith(".py"):
                path = parent_path + ":" + node_name
            else:
                path = parent_path + "." + node_name

        lineno = None
        if hasattr(node, "lineno"):
            lineno = node.lineno
            # Python 3.8+ fixed the line number calc for decorated functions;
            # previously the AST node would report the line number of the
            # decorator, not the obj itself. We're going to try and back-port.
            if not PY_38_HIGHER:
                if hasattr(node, "decorator_list"):
                    lineno += len(node.decorator_list)

        end_lineno = None
        if hasattr(node, "end_lineno"):
            end_lineno = node.end_lineno

        if not self._has_doc(node):
            source = self._get_source_code(self.source, node)
            docstring = self._make_docstring_node(source)
            # TODO: Pass this to ChatGPT
            node.body.insert(0, docstring)

        return node
        # node_type = type(node).__name__
        # docs_node = DocsNode(
        #     name=node_name,
        #     path=path,
        #     covered=self._has_doc(node),
        #     source_code=self._get_source_code(self.source, node),
        #     level=len(self.stack),
        #     node_type=node_type,
        #     lineno=lineno,
        #     end_lineno=end_lineno,
        #     is_nested_func=self._is_nested_func(parent, node_type),
        #     is_nested_cls=self._is_nested_cls(parent, node_type),
        #     parent=parent,
        # )
        # self.stack.append(docs_node)
        # self.nodes.append(docs_node)
        #
        # self.generic_visit(node)
        #
        # self.stack.pop()

    def _is_nested_func(self, parent, node_type):
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested function?
        if parent.node_type == "FunctionDef" and node_type == "FunctionDef":
            return True
        return False

    def _is_nested_cls(self, parent, node_type):
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested class?
        if (
            parent.node_type in ("ClassDef", "FunctionDef")
            and node_type == "ClassDef"
        ):
            return True
        return False

    def _is_private(self, node):
        """Is node private (i.e. __MyClass, __my_func)."""
        if node.name.endswith("__"):
            return False
        if not node.name.startswith("__"):
            return False
        return True

    def _is_semiprivate(self, node):
        """Is node semiprivate (i.e. _MyClass, _my_func)."""
        if node.name.endswith("__"):
            return False
        if node.name.startswith("__"):
            return False
        if not node.name.startswith("_"):
            return False
        return True

    def _is_ignored_common(self, node):
        """Commonly-shared ignore checkers."""
        is_private = self._is_private(node)
        is_semiprivate = self._is_semiprivate(node)

        if self.config.ignore_private and is_private:
            return True
        if self.config.ignore_semiprivate and is_semiprivate:
            return True

        if self.config.ignore_regex:
            for regexp in self.config.ignore_regex:
                regex_result = regexp.match(node.name)
                if regex_result:
                    return True
        return False

    def _has_property_decorators(self, node):
        """Detect if node has property get/setter decorators."""
        if not hasattr(node, "decorator_list"):
            return False

        for dec in node.decorator_list:
            if hasattr(dec, "id"):
                if dec.id == "property":
                    return True
            if hasattr(dec, "attr"):
                if dec.attr == "setter":
                    return True
        return False

    def _has_setters(self, node):
        """Detect if node has property get/setter decorators."""
        if not hasattr(node, "decorator_list"):
            return False

        for dec in node.decorator_list:
            if hasattr(dec, "attr"):
                if dec.attr == "setter":
                    return True
        return False

    def _is_func_ignored(self, node):
        """Should the AST visitor ignore this func/method node."""
        is_init = node.name == "__init__"
        is_magic = all(
            [
                node.name.startswith("__"),
                node.name.endswith("__"),
                node.name != "__init__",
            ]
        )
        has_property_decorators = self._has_property_decorators(node)
        has_setters = self._has_setters(node)

        if self.config.ignore_init_method and is_init:
            return True
        if self.config.ignore_magic and is_magic:
            return True
        if self.config.ignore_property_decorators and has_property_decorators:
            return True
        if self.config.ignore_property_setters and has_setters:
            return True

        return self._is_ignored_common(node)

    def _is_class_ignored(self, node):
        """Should the AST visitor ignore this class node."""
        return self._is_ignored_common(node)

    def visit_ClassDef(self, node):
        """Visit class for docstrings.

        :param ast.ClassDef node: a class AST node.
        """
        if self._is_class_ignored(node):
            return
        self._visit_helper(node)

    def visit_FunctionDef(self, node):
        """Visit function or method for docstrings.

        :param ast.FunctionDef node: a function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function or method for docstrings.

        :param ast.AsyncFunctionDef node: a async function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)
