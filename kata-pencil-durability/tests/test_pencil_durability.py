import pytest
from kata_pencil_durability.src.eraser import Eraser
from kata_pencil_durability.src.paper import Paper
from kata_pencil_durability.src.pencil import Pencil
from kata_pencil_durability import constants

import collections
PaperEraser = collections.namedtuple('PaperEraser', 'paper eraser')
PencilPaper = collections.namedtuple('PencilPaper', 'pencil paper')


@pytest.fixture(scope="module", autouse=True)
def paper_tests():
    paper_obj = Paper()
    return paper_obj


@pytest.fixture(scope="module", autouse=True)
def eraser_tests():
    eraser_obj = PaperEraser(Paper(), Eraser(durability=1000))
    return eraser_obj


@pytest.fixture(scope="module", autouse=True)
def pencil_tests():
    pencil_obj = PencilPaper(Pencil(point_durability=2000, length=30), Paper())
    return pencil_obj


@pytest.mark.skipif(not Paper, reason="Instance not available")
def test_check_empty_paper(paper_tests):
    assert paper_tests.text == ''


def test_set_paper_text(paper_tests):
    paper_tests.text = 'sample'
    assert paper_tests.text == 'sample'


@pytest.mark.skipif(not Eraser, reason="Instance not available")
def test_paper_index_out_of_bounds(eraser_tests):
    eraser_tests.paper.text = 'TEST'
    eraser_tests.eraser._erase_char_val(eraser_tests.paper, index=len(eraser_tests.paper.text) + 1)
    assert eraser_tests.paper.text == 'TEST'


def test_write_erase_char(eraser_tests):
    eraser_tests.paper.text = 'TEAM'
    eraser_tests.eraser.erase('T', paper=eraser_tests.paper)
    assert eraser_tests.paper.text == (constants.space_char + 'EAM')


def test_erase_text_by_replacing_with_empty_spaces(eraser_tests):
    eraser_tests.paper.text = "Test Pencil Durability"
    eraser_tests.eraser.erase('Pencil', eraser_tests.paper)
    assert eraser_tests.paper.text == "Test " + constants.space_char * len('Pencil') + " Durability"


def test_erase_last_occurence_of_text(eraser_tests):
    eraser_tests.paper.text = "How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
    eraser_tests.eraser.erase('chuck', eraser_tests.paper)
    assert eraser_tests.paper.text == "How much wood would a woodchuck chuck if a woodchuck could       wood?"

    eraser_tests.eraser.erase('chuck', eraser_tests.paper)
    assert eraser_tests.paper.text == "How much wood would a woodchuck chuck if a wood      could       wood?"


def test_paper_does_not_contain_text_to_erase(eraser_tests):
    eraser_tests.paper.text = 'Dhanu'
    eraser_tests.eraser.erase('Surisetty', eraser_tests.paper)
    assert eraser_tests.paper.text == 'Dhanu'


def test_erase_text_right_to_left(eraser_tests):
    eraser_tests.paper.text = 'Buffalo Bill'
    eraser_tests.eraser.durability = 3

    eraser_tests.eraser.erase('Bill', eraser_tests.paper)
    assert eraser_tests.paper.text == 'Buffalo B' + (3 * constants.space_char)


def test_degrade_by_one_for_non_space(eraser_tests):
    initial_eraser_durability = eraser_tests.eraser.durability
    eraser_tests.paper.text = 'A'
    eraser_tests.eraser._erase_char_val(paper=eraser_tests.paper, index=0)

    assert eraser_tests.eraser.durability == initial_eraser_durability


def test_degrade_by_zero_if_char_is_space(eraser_tests):
    initial_eraser_durability = eraser_tests.eraser.durability
    eraser_tests.paper.text = ' '

    eraser_tests.eraser._erase_char_val(paper=eraser_tests.paper, index=0)
    assert eraser_tests.eraser.durability == initial_eraser_durability


def test_degrade_by_two_when_erasing_two_characters(eraser_tests):
    eraser_tests.paper.text = 'AA'

    eraser_tests.eraser.erase('AA', eraser_tests.paper)
    assert eraser_tests.eraser.durability == 0


def test_write_text_to_paper(pencil_tests):
    text_to_write = 'dhanu'

    pencil_tests.pencil.write_data(text_to_write, pencil_tests.paper)
    assert pencil_tests.paper.text == text_to_write


def test_append_text_to_paper(pencil_tests):
    pencil_tests.paper.text = 'She sells sea shells'
    text_to_append = ' down by the sea shore'
    pencil_tests.pencil.write_data(text_to_append, pencil_tests.paper)

    assert pencil_tests.paper.text == 'She sells sea shells down by the sea shore'
