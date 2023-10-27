import ast
import os
import textwrap

import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from gpt4docstrings.docstring import Docstring
from gpt4docstrings.docstrings_translators.base import DocstringTranslator
from gpt4docstrings.prompts.translation.chatgpt import PROMPT
from gpt4docstrings.utils.decorators import retry
from gpt4docstrings.utils.parsers import DocstringParser
from gpt4docstrings.visit import GPT4DocstringsNode


class ChatGPTDocstringTranslator(DocstringTranslator):
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

        self.model = ChatOpenAI(
            model_name=model_name, temperature=1.0, openai_api_key=self.api_key
        )
        self.prompt_template = PROMPT

    async def _get_completion(self, prompt: str) -> str:
        """
        Generates a completion using the ChatGPT model.

        Args:
            prompt (str): The prompt for generating the completion.

        Returns:
            str: The generated completion.
        """
        return await self.model.apredict(prompt)

    @retry()
    async def translate_docstring(self, node: GPT4DocstringsNode) -> Docstring:
        """
        Translates a docstring for a function.

        Args:
            node (GPT4DocstringsNode): A GPT4DocstringsNode node

        Returns:
            Docstring: A Docstring object
        """
        docstring = ast.get_docstring(node.ast_node)
        stripped_source = textwrap.dedent(docstring)
        parent_offset = node.col_offset

        prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["docstring", "style"],
        )
        _input = prompt.format_prompt(
            docstring=stripped_source, style=self.docstring_style
        )
        docstring = DocstringParser().parse(
            await self._get_completion(_input.to_string())
        )

        return Docstring(
            text=docstring, col_offset=4 + parent_offset, lineno=node.docstring_lineno
        )
