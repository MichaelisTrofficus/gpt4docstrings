import asyncio


async def async_example():
    await asyncio.sleep(2)


class MyClass:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def nested_method():
        def inner_function():
            print("Nested method inner function")

        print("Nested method start")
        inner_function()
        print("Nested method completed")
