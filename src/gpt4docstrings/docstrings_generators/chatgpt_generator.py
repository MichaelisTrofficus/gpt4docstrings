import os
import re
import textwrap
import time

import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.prompt import PromptValue
from redbaron import RedBaron

from gpt4docstrings.docstrings_generators.utils.parsers import FunctionDocstringParser
from gpt4docstrings.docstrings_generators.utils.prompts import CLASS_PROMPTS
from gpt4docstrings.docstrings_generators.utils.prompts import FUNCTION_PROMPTS


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

    def _get_completion(self, prompt: PromptValue) -> str:
        """
        Generates a completion using the ChatGPT model.

        Args:
            prompt (PromptValue): The prompt for generating the completion.

        Returns:
            str: The generated completion.
        """
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                return self.model.predict(prompt.to_string()).strip()
            except openai.error.APIError:
                time.sleep(5)
                retries += 1
            except openai.error.ServiceUnavailableError:
                time.sleep(5)
                retries += 1

    def generate_function_docstring(self, source: str) -> dict:
        """
        Generates a docstring for a function.

        Args:
            source (str): The source code of the function.

        Returns:
            dict: A dictionary containing the generated docstring.
        """
        source = source.strip()
        stripped_source = textwrap.dedent(source)
        prompt = PromptTemplate(
            template=self.function_prompt_template,
            input_variables=["code"],
        )
        _input = prompt.format_prompt(code=stripped_source)
        fn_src = FunctionDocstringParser().parse(self._get_completion(_input))
        fn_node = RedBaron(fn_src)[0]
        return {
            "docstring": {
                "text": '"""' + textwrap.dedent(fn_node[0].to_python()) + '"""',
                "indentation_level": len(fn_node[0].indentation),
            }
        }

    def generate_class_docstring(self, source: str) -> dict:
        """
        Generates docstrings for a class.

        Args:
            source (str): The source code of the class.

        Returns:
            dict: A dictionary containing the generated docstrings.
        """
        source = source.strip()
        stripped_source = textwrap.dedent(source)

        system_role = (
            "When you are asked to generate Python docstrings for a class "
            "only return the class with the generated docstrings."
        )
        prompt = (
            f"Write Python docstrings [in {self.docstring_style} style] for the Python class below. \n\n"
            f"1. Output with no introduction, no explanation, only code. \n"
            f"2. Don't make mistakes and check if you did.\n"
            f"3. Only return Python3 code and the docstrings, and nothing else. \n"
            f"4. Check if the generated docstrings follow [{self.docstring_style} style]. If not, translate them into "
            f"[{self.docstring_style} style].\n\n"
            f"{stripped_source}\n"
            f"Code: "
        )

        docstrings = {}
        generated_docstring = self._get_completion(prompt, system_role)

        if generated_docstring.strip().startswith("```python"):
            match = re.search(
                r"```python(.+?)```", generated_docstring, flags=re.DOTALL
            )
            generated_docstring = match.group(1).strip()

        class_source = RedBaron(generated_docstring)
        class_node = class_source[0]
        method_nodes = [f for f in class_node.find_all("def")]

        for method_node in method_nodes:
            docstrings[method_node.name] = method_node.value[0]

        docstrings["docstring"] = class_node.value[0]

        return docstrings
