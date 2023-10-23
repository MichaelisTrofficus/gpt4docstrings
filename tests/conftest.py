import os

import pytest


def pytest_configure():
    pytest.TESTS_PATH = os.path.dirname(__file__)


@pytest.fixture(scope="module")
def test_openai_api_key() -> pytest.fixture():
    os.environ["OPENAI_API_KEY"] = "test_api_key"
