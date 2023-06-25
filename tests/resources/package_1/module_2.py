class A:
    def __init__(self, attr1: str, attr2: int):
        self.attr1 = attr1
        self.attr2 = attr2

    def add_word_to_attr1(self, word: str):
        return word + self.attr1

    def pow_attr2(self):
        return self.attr2**2
