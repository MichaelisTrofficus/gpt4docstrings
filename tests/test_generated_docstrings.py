import os

import pytest
from redbaron import RedBaron

from gpt4docstrings import GPT4Docstrings
from gpt4docstrings import utils


def test_all_docstrings(tmp_path, mocker, write_source_side_effect):
    tmp_file = tmp_path / "test.py"

    mocker.patch(
        "gpt4docstrings.docstrings_generator.utils.write_updated_source_to_file",
        return_value=None,
        side_effect=write_source_side_effect(tmp_file),
    )

    docstrings_generator = GPT4Docstrings(
        paths=[os.path.join(pytest.TESTS_PATH, "resources")]
    )
    docstrings_generator.generate_docstrings()

    source = RedBaron(open(tmp_file, encoding="utf-8").read())

    for node in source.find_all("def"):
        if not utils.check_def_node_is_class_method(node):
            assert (
                node.value[0].value
                == '"""\n    This is a generated docstring!!\n    """'
            )

    for node in source.find_all("class"):
        assert (
            node.value[0].value == '"""\n    This is a generated docstring!!\n    """'
        )

        for method_node in node.value:
            if (
                method_node.type == "def"
                and method_node.name
                not in docstrings_generator.excluded_special_methods
            ):
                assert (
                    method_node.value[0].value
                    == '"""\n    \tThis is a generated docstring!!\n    \t"""'
                )
