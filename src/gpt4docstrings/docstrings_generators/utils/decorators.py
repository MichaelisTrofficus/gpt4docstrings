import time

import openai


def retry(max_retries, delay):
    """Decorator for retrying a function with a specified number of retries and delay between retries."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (openai.error.APIError, openai.error.ServiceUnavailableError):
                    time.sleep(delay)
                    retries += 1
            raise Exception(f"Max retries ({max_retries}) exceeded.")

        return wrapper

    return decorator
