import asyncio
import logging

from gpt4docstrings.exceptions import DocstringParsingError


def retry(max_retries=5, delay=5):
    """Decorator for retrying a function with a specified number of retries and delay between retries."""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (DocstringParsingError, SyntaxError) as e:
                    logging.warning(e)
                    retries += 1
                    if retries >= max_retries:
                        raise Exception(f"Max retries ({max_retries}) exceeded.")
                    await asyncio.sleep(delay)

        return wrapper

    return decorator
