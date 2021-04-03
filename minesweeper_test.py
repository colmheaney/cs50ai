import pytest
from minesweeper import MinesweeperAI, Sentence

def test_sentence_known_safes():
  safe_sentence = Sentence({(0,0), (1,1)}, 0)
  assert(safe_sentence.known_safes()) == { (0,0), (1,1) }

  not_safe_sentence = Sentence({(0,0), (1,1)}, 1)
  assert(not_safe_sentence.known_safes()) == {}


def test_sentence_known_mines():
  mines_sentence = Sentence({(0,0), (1,1)}, 2)
  assert(mines_sentence.known_mines()) == { (0,0), (1,1) }

  no_mines_sentence = Sentence({(0,0), (1,1)}, 1)
  assert(no_mines_sentence.known_mines()) == {}


def test_sentence_mark_mine_valid_cell():
  sentence = Sentence({(0,0), (1,1)}, 2)
  sentence.mark_mine((0,0))
  assert(sentence.__str__()) == "{(1, 1)} = 1"


def test_sentence_mark_mine_invalid_cell():
  sentence = Sentence({(0,0), (1,1)}, 2)
  sentence.mark_mine((3,0))
  assert(sentence.__str__()) == "{(1, 1), (0, 0)} = 2"


def test_sentence_mark_safe_valid_cell():
  sentence = Sentence({(0,0), (1,1), (2,2)}, 2)
  sentence.mark_safe((0,0))
  assert(sentence.__str__()) == "{(1, 1), (2, 2)} = 2"


def test_sentence_mark_safe_invalid_cell():
  sentence = Sentence({(0,0), (1,1), (2,2)}, 2)
  sentence.mark_safe((3,0))
  assert(sentence.__str__()) == "{(0, 0), (1, 1), (2, 2)} = 2"