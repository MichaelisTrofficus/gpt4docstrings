import os

import pytest

from gpt4docstrings import GPT4Docstrings


def test_find_all_functions(test_openai_api_key):
    docstrings_generator = GPT4Docstrings(
        paths=[os.path.join(pytest.TESTS_PATH, "resources/")]
    )
    py_files = docstrings_generator.get_filenames_from_paths()
    assert set(py_files) == {
        f"{pytest.TESTS_PATH}/resources/module_1.py",
        f"{pytest.TESTS_PATH}/resources/package_1/module_2.py",
    }


def test_exclude_functions(test_openai_api_key):
    docstrings_generator = GPT4Docstrings(
        paths=[os.path.join(pytest.TESTS_PATH, "resources")],
        excluded=[os.path.join(pytest.TESTS_PATH, "resources/package_1/*")],
    )
    py_files = docstrings_generator.get_filenames_from_paths()
    assert set(py_files) == {f"{pytest.TESTS_PATH}/resources/module_1.py"}
