import pytest
from tictactoe import X, O, EMPTY
from tictactoe import player, actions, result, winner, terminal, utility, minimax


def test_player_initial():
  assert player([[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]) == X


def test_player_X_turn():
  assert player([[EMPTY, EMPTY, O],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]) == X


def test_player_O_turn():
  assert player([[EMPTY, EMPTY, EMPTY],
                 [EMPTY, X, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]) == O


def test_actions_all_empty():
  result = {(0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)}

  assert actions([[EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY],
                  [EMPTY, EMPTY, EMPTY]]) == result


def test_actions_not_empty():
  result = {(0,0),(2,1)}

  assert actions([[EMPTY, X, O],
                  [O, X, X],
                  [X, EMPTY, O]]) == result


def test_actions_terminal():
  result = set()

  assert actions([[X, X, O],
                  [O, X, X],
                  [O, O, X]]) == result


def test_result():
  action = (0,0)
  result_board = [[O,X,O],
                  [O,X,X],
                  [X,EMPTY,O]]

  inital_board = [[EMPTY,X,O],
                  [O,X,X],
                  [X,EMPTY,O]]

  assert result(inital_board, action) == result_board
  assert inital_board == [[EMPTY,X,O],
                          [O,X,X],
                          [X,EMPTY,O]]


def test_result_invalid_move():
  with pytest.raises(Exception):
    action = (2,2)
    result_board = [[X,O,X],
                    [O,X,O],
                    [X,O,X]]

    assert result([[X,O,X],
                   [O,X,O],
                   [X,O,X]], action) == result_board


def test_winner():
  assert winner([[X,X,X],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]) == X
  assert winner([[EMPTY,EMPTY,EMPTY],[X,X,X],[EMPTY,EMPTY,EMPTY]]) == X
  assert winner([[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [X,X,X]]) == X
  assert winner([[O,O,O], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]) == O
  assert winner([[EMPTY, EMPTY, EMPTY], [O,O,O], [EMPTY, EMPTY, EMPTY]]) == O
  assert winner([[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [O,O,O]]) == O

  assert winner([[X,EMPTY,EMPTY],[X, EMPTY, EMPTY],[X, EMPTY, EMPTY]]) == X
  assert winner([[EMPTY,X,EMPTY],[EMPTY, X, EMPTY],[EMPTY, X, EMPTY]]) == X
  assert winner([[EMPTY,EMPTY,X],[EMPTY, EMPTY,X],[EMPTY, EMPTY,X]]) == X
  assert winner([[O,EMPTY,EMPTY],[O, EMPTY, EMPTY],[O, EMPTY, EMPTY]]) == O
  assert winner([[EMPTY,O,EMPTY],[EMPTY, O, EMPTY],[EMPTY, O, EMPTY]]) == O
  assert winner([[EMPTY,EMPTY,O],[EMPTY, EMPTY,O],[EMPTY, EMPTY,O]]) == O

  assert winner([[X,EMPTY,EMPTY], [EMPTY, X,EMPTY], [EMPTY, EMPTY,X]]) == X
  assert winner([[O,EMPTY,EMPTY], [EMPTY,O,EMPTY], [EMPTY, EMPTY,O]]) == O

  assert winner([[X,X,O], [O,O,X], [X,O,X]]) == None


def test_terminal_winner():
  assert terminal([[O,EMPTY,X],
                   [O,X,EMPTY],
                   [X,O,X]]) == True


def test_terminal_no_winner():
  assert terminal([[X,O,O],
                   [O,X,X],
                   [O,X,O]]) == True


def test_terminal_not_finished():
  assert terminal([[O,EMPTY,EMPTY],
                   [O,X,EMPTY],
                   [X,O,X]]) == False


def test_utility_X():
  assert utility([[O,EMPTY,X],
                  [O,X,EMPTY],
                  [X,O,X]]) == 1


def test_utility_O():
  assert utility([[O,X,X],
                  [X,O,EMPTY],
                  [O,X,O]]) == -1


def test_utility_no_winner():
  assert utility([[X,X,O],
                  [O,O,X],
                  [X,O,X]]) == 0


def test_minimax_1():
  assert minimax([[EMPTY,X,O],
                  [O,X,X],
                  [X,EMPTY,O]]) == (2,1)


def test_minimax_2():
  assert minimax([[O,X,O],
                  [O,X,X],
                  [X,EMPTY,O]]) == (2,1)


def test_minimax_3():
  assert minimax([[EMPTY,X,O],
                  [O,X,EMPTY],
                  [X,EMPTY,O]]) == (2,1)