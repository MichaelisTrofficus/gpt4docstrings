import os
import textwrap

import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from redbaron import RedBaron

from gpt4docstrings import utils
from gpt4docstrings.docstrings_generators.utils.decorators import retry
from gpt4docstrings.docstrings_generators.utils.parsers import DocstringParser
from gpt4docstrings.docstrings_generators.utils.prompts import CLASS_PROMPTS
from gpt4docstrings.docstrings_generators.utils.prompts import FUNCTION_PROMPTS
from gpt4docstrings.exceptions import ASTError


class ChatGPTDocstringGenerator:
    """A class for generating Python docstrings using ChatGPT."""

    def __init__(
        self,
        api_key: str,
        model_name: str,
        docstring_style: str,
    ):
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please, provide the OpenAI API Key")

        openai.api_key = self.api_key

        self.model_name = model_name
        self.docstring_style = docstring_style

        self.model = ChatOpenAI(model_name=model_name, temperature=1.0)
        self.function_prompt_template = FUNCTION_PROMPTS.get(docstring_style)
        self.class_prompt_template = CLASS_PROMPTS.get(docstring_style)

    @retry(max_retries=5, delay=5)
    def _get_completion(self, prompt: str) -> str:
        """
        Generates a completion using the ChatGPT model.

        Args:
            prompt (str): The prompt for generating the completion.

        Returns:
            str: The generated completion.
        """
        return self.model.predict(prompt).strip()

    def generate_function_docstring(self, source: str) -> dict:
        """
        Generates a docstring for a function.

        Args:
            source (str): The source code of the function.

        Returns:
            dict: A dictionary containing the generated docstring.

        Raises:
            ASTError: Raises an ASTError when there are errors interacting with an AST node
        """
        source = source.strip()
        stripped_source = textwrap.dedent(source)
        prompt = PromptTemplate(
            template=self.function_prompt_template,
            input_variables=["code"],
        )
        _input = prompt.format_prompt(code=stripped_source)
        fn_src = DocstringParser().parse(self._get_completion(_input.to_string()))

        try:
            fn_node = RedBaron(fn_src)[0]
            return {
                "docstring": utils.add_indentation_to_docstring(
                    '"""' + textwrap.dedent(fn_node[0].to_python()) + '"""',
                    fn_node[0].indentation,
                )
            }
        except ValueError as e:
            raise ASTError(
                f"Some error has occurred when trying to parse the current AST node: {e}"
            ) from e

    def generate_class_docstring(self, source: str) -> dict:
        """
        Generates docstrings for a class.

        Args:
            source (str): The source code of the class.

        Returns:
            dict: A dictionary containing the generated docstrings.

        Raises:
            ASTError: Raises an ASTError when there are errors interacting with an AST node
        """
        source = source.strip()
        stripped_source = textwrap.dedent(source)
        prompt = PromptTemplate(
            template=self.class_prompt_template,
            input_variables=["code"],
        )
        _input = prompt.format_prompt(code=stripped_source)
        class_src = DocstringParser().parse(self._get_completion(_input.to_string()))

        try:
            class_node = RedBaron(class_src)[0]
            method_nodes = [f for f in class_node.find_all("def")]

            docstrings = {}
            for method_node in method_nodes:
                docstrings[method_node.name] = utils.add_indentation_to_docstring(
                    '"""' + textwrap.dedent(method_node[0].to_python()) + '"""',
                    method_node[0].indentation,
                )

            docstrings["docstring"] = class_node.value[0]
            docstrings["docstring"] = utils.add_indentation_to_docstring(
                '"""' + textwrap.dedent(class_node[0].to_python()) + '"""',
                class_node[0].indentation,
            )

            return docstrings

        except ValueError as e:
            raise ASTError(
                f"Some error has occurred when trying to parse the current AST node: {e}"
            ) from e
