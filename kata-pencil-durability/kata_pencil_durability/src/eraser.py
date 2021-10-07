from kata_pencil_durability import constants


class Eraser:

    def __init__(self, durability: int = 0):
        self.durability = durability

    def erase(self, text, paper):
        index = paper.text.rfind(text)

        if index < 0:
            return

        for i in reversed(range(0, len(text))):
            self._erase_char_val(paper, index + i)

    def _erase_char_val(self, paper, index):
        if self.durability == 0 or index >= len(paper.text):
            return

        self.durability -= constants.zero if paper.text[index].isspace() else constants.one

        paper.text = paper.text[:index] + constants.space_char + paper.text[index + 1:]
        paper.last_erased = index
