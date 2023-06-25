import os

import pytest


def pytest_configure():
    pytest.TESTS_PATH = os.path.dirname(__file__)


@pytest.fixture
def write_source_side_effect():
    def _write_source_side_effect(filename):
        def __write_source_side_effect(_source, _filename):
            _filename = filename
            with open(_filename, "a", encoding="utf-8") as file:
                file.write(_source.dumps())

        return __write_source_side_effect

    return _write_source_side_effect
