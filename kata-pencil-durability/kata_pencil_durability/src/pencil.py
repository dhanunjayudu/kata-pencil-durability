__author__ = 'Dhanu'

import logging
from kata_pencil_durability import constants

log = logging.getLogger(__name__)


class Pencil:

    def __init__(self, point_durability: int = 0, length: int = 0):
        self.__point_durability = point_durability
        self.__length = length

    def write_data(self, text, paper):
        log.info(f'text value={text}')
        for char in text:
            self._write_char(char=char, index=len(paper.text), paper=paper)

    def _write_char(self, char, index, paper):
        log.info(f'char value={char}')
        if self.__point_durability < self._calculate_write_char(char):
            char = constants.space_char
        elif self._is_override(index, paper):
            char = constants.collision_char

        paper.text = paper.text[:index] + char + paper.text[index + 1:]

        self.__point_durability -= self._calculate_write_char(char)

    def _is_override(self, index, paper):
        return not index > len(paper.text) - 1 and not paper.text[index].isspace()

    def _calculate_write_char(self, char):
        if char.isupper() or char.isnumeric():
            return constants.two
        elif char.islower():
            return constants.one
        else:
            return constants.zero

    def sharpen_pencil(self):
        if self.__length == 0:
            return

        self.__length -= 1

    def edit_data(self, text, paper):
        index = paper.last_erased

        if index == constants.last_erased:
            self.write_data(text, paper)
            return

        for char in text:
            self._write_char(char, index, paper)
            index += 1
