def fn(a, b):
    return a + b


def fn2(a, b):
    return a * b


class A:
    def __init__(self):
        print(1)

    @staticmethod
    def f1():
        return 1

    @staticmethod
    def f2():
        return 0
