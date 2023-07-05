"""Sphinx configuration."""
project = "gpt4docstrings"
author = "Miguel Otero Pedrido"
copyright = "2023, Miguel Otero Pedrido"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.autosummary",
    "myst_parser",
    "sphinx_click",
]

todo_include_todos = False
add_function_parentheses = True
pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"
