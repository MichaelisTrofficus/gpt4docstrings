import os
import re
import textwrap
import time

import openai
from redbaron import RedBaron

from gpt4docstrings.utils import match_between_characters


class ChatGPTDocstringGenerator:
    """A class for generating Python docstrings using ChatGPT."""

    def __init__(
        self,
        api_key: str,
        model: str,
        docstring_style: str,
    ):
        self.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        self.model = model
        self.docstring_style = docstring_style

        if not self.api_key:
            raise ValueError("Please, provide the OpenAI API Key")

        openai.api_key = self.api_key

    def _get_completion(self, prompt: str, system_role: str) -> str:
        """
        Generates a completion using the ChatGPT model.

        Args:
            prompt (str): The prompt for generating the completion.
            system_role (str): The role of the system in the conversation.

        Returns:
            str: The generated completion.
        """
        max_retries = 5
        retries = 0
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt},
        ]

        while retries < max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=0,
                )
                return response.choices[0].message["content"]
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

        system_role = "When you generate Python docstrings only return a string that I can add to my code."
        prompt = (
            f"Write a Python docstring [in {self.docstring_style}-style format] for the piece of code "
            f"delimited by triple backticks.\n\n"
            f"1. Output with no introduction, no explanation, only the docstring. \n"
            f"2. Don't make mistakes and check if you did.\n"
            f"3. Return the generated docstring as a string, so I can copy it and add it as a docstring to my code.\n"
            f"4. Don't return Python code, only the generated docstring. \n\n"
            f"5. Check if the generated docstring follows [{self.docstring_style}-style format]. If not, translate "
            f"it into [{self.docstring_style}-style format].\n\n"
            f"```\n"
            f"{stripped_source}\n"
            f"```\n"
        )
        generated_docstring = self._get_completion(prompt, system_role)
        if generated_docstring.startswith("```python"):
            generated_docstring = match_between_characters(
                generated_docstring, start_char="```python", end_char="```"
            )

        try:
            node = RedBaron(generated_docstring)
            if node[0].type == "def":
                generated_docstring = node[0].value[0].value.strip()
        except Exception as e:
            print(e)

        return {"docstring": generated_docstring}

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
