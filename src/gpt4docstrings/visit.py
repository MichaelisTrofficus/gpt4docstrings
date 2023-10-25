# Copyright 2020 Lynn Root
# This code comes from Lynn Root's interrogate amazing library
# https://github.com/econchick/interrogate
import ast
import os
import sys

import attr


PY_38_HIGHER = sys.version_info >= (3, 8)


@attr.s(eq=False)
class GPT4DocstringsNode:
    """
    This class contains digestible information about the AST node. We'll
    use this information to generate the docstrings.

    Args:
        name (str): Name of node (module, class, method, or function names).
        path (str): Pseudo-import path to the node (e.g., "sample.py:MyClass.my_method").
        source (str): The source code of the function / class
        level (int): Level of recursiveness/indentation.
        covered (bool): Indicates whether the node has a docstring.
        node_type (str): Type of node (e.g., "module," "class," or "function")
        is_nested_func (bool): Specifies if the node is a nested function or method.
        is_nested_cls (bool): Specifies if the node is a nested class.
        is_cls_method (bool): Specifies if the node is a Class method.
        parent (NodeInfo): Parent node of the current DocsNode, if any.

    Returns:
        None
    """

    name = attr.ib()
    path = attr.ib()
    source = attr.ib()
    ast_node = attr.ib()
    level = attr.ib()
    docstring_lineno = attr.ib()
    col_offset = attr.ib()
    covered = attr.ib()
    node_type = attr.ib()
    is_nested_func = attr.ib()
    is_nested_cls = attr.ib()
    is_cls_method = attr.ib()
    parent = attr.ib()


class GPT4DocstringsVisitor(ast.NodeVisitor):
    """
    NodeVisitor for a Python file to find docstrings.

    Args:
        filename (str): filename to parse coverage
        config (GPT4DocstringsConfig): configuration
    """

    def __init__(self, filename, config):
        self.filename = filename
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
    def _get_col_offset(node):
        """Gets the column offset necessary to be applied to the docstring"""
        try:
            return node.col_offset
        except AttributeError:
            return None

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

        docstring_lineno = None
        if (
            hasattr(node, "body")
            and len(node.body) > 0
            and hasattr(node.body[0], "lineno")
        ):
            docstring_lineno = node.body[0].lineno - 1

        node_type = type(node).__name__
        cov_node = GPT4DocstringsNode(
            name=node_name,
            path=path,
            source=ast.unparse(node),
            ast_node=node,
            covered=self._has_doc(node),
            level=len(self.stack),
            node_type=node_type,
            docstring_lineno=docstring_lineno,
            col_offset=self._get_col_offset(node),
            is_nested_func=self._is_nested_func(parent, node_type),
            is_nested_cls=self._is_nested_cls(parent, node_type),
            is_cls_method=self._is_cls_method(parent, node_type),
            parent=parent,
        )
        self.stack.append(cov_node)
        self.nodes.append(cov_node)

        self.generic_visit(node)

        self.stack.pop()

    @staticmethod
    def _is_cls_method(parent, nodetype):
        """Is node a method belonging to a class."""
        if parent is None:
            return False
        if parent.node_type == "ClassDef" and nodetype == "FunctionDef":
            return True
        return False

    @staticmethod
    def _is_nested_func(parent, node_type):
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested function?
        if parent.node_type == "FunctionDef" and node_type == "FunctionDef":
            return True
        return False

    @staticmethod
    def _is_nested_cls(parent, node_type):
        """Is node a nested func/method of another func/method."""
        if parent is None:
            return False
        # is it a nested class?
        if parent.node_type in ("ClassDef", "FunctionDef") and node_type == "ClassDef":
            return True
        return False

    @staticmethod
    def _is_private(node):
        """Is node private (i.e. __MyClass, __my_func)."""
        if node.name.endswith("__"):
            return False
        if not node.name.startswith("__"):
            return False
        return True

    @staticmethod
    def _is_semiprivate(node):
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

        return False

    @staticmethod
    def _has_property_decorators(node):
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

    @staticmethod
    def _has_setters(node):
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
        has_property_decorators = self._has_property_decorators(node)
        has_setters = self._has_setters(node)

        if self.config.ignore_init_method and is_init:
            return True
        if self.config.ignore_property_decorators and has_property_decorators:
            return True
        if self.config.ignore_property_setters and has_setters:
            return True

        return self._is_ignored_common(node)

    def _is_class_ignored(self, node):
        """Should the AST visitor ignore this class node."""
        return self._is_ignored_common(node)

    def visit_Module(self, node):
        """
        Visit module for docstrings.

        :param ast.Module node: a module AST node.
        """
        self._visit_helper(node)

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

        :param ast.AsyncFunctionDef node: an async function/method AST node.
        """
        if self._is_func_ignored(node):
            return
        self._visit_helper(node)
