import attr
from interrogate.config import InterrogateConfig


@attr.s
class GPT4DocstringsConfig(InterrogateConfig):
    """
    Default config for GPT4Docstrings. It will ignore by default module, init methods
    and init modules. It will also use by default `gpt-3.5-turbo` model.
    """
    llm = attr.ib(default="gpt-3.5-turbo")
