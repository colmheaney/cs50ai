"""
Tic Tac Toe Player
"""

import math
import copy
from random import randrange

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = []
    for row in board:
        flat_board.extend(row)

    if flat_board.count(X) <= flat_board.count(O):
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in enumerate(board):
        for j in enumerate(i[1]):
            if j[1] == EMPTY:
                actions.add((i[0],j[0]))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    next_board = copy.deepcopy(board)
    next_player = player(board)
    if next_board[action[0]][action[1]] != EMPTY:
        raise Exception('Invalid Move')

    next_board[action[0]][action[1]] = next_player
    return next_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    """
    Check rows
    """
    for row in board:
        if row.count(X) == 3: return X
        if row.count(O) == 3: return O

    """
    Check diags
    """
    if board[1][1] == X and (
        (board[0][0] == X and board[2][2] == X) or
        (board[0][2] == X and board[2][0] == X)): return X
    if board[1][1] == O and (
        (board[0][0] == O and board[2][2] == O) or
        (board[0][2] == O and board[2][0] == O)): return O

    """
    Check columns
    """
    if (board[0][0] == X and board[1][0] == X and board[2][0] == X or
        board[0][1] == X and board[1][1] == X and board[2][1] == X or
        board[0][2] == X and board[1][2] == X and board[2][2] == X): return X
    if (board[0][0] == O and board[1][0] == O and board[2][0] == O or
        board[0][1] == O and board[1][1] == O and board[2][1] == O or
        board[0][2] == O and board[1][2] == O and board[2][2] == O): return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result = winner(board)
    if (result == X or
        result == O or
        not __empty_spaces(board)): return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if   result == X: return  1
    elif result == O: return -1
    else:             return  0



def minimax(board):
    score_dict = {}

    if board == initial_state():
        return((randrange(3),randrange(3)))

    __minimax(board, 1, score_dict)

    if player(board) == X:
        return max(score_dict, key=score_dict.get)
    else:
        return min(score_dict, key=score_dict.get)


def __minimax(board, depth, score_dict):
    if terminal(board):
        return utility(board)

    if player(board) == X:
        maxEval = float('-inf')

        for action in actions(board):
            eval = __minimax(result(board, action), depth+1, score_dict)
            maxEval = max(eval, maxEval)
            if depth == 1:
                score_dict[action] = maxEval
        return maxEval

    else:
        minEval = float('inf')

        for action in actions(board):
            eval = __minimax(result(board, action), depth+1, score_dict)
            minEval = min(eval, minEval)
            if depth == 1:
                score_dict[action] = minEval
        return minEval


def __empty_spaces(board):
    for row in board:
        if row.count(EMPTY) != 0: return True

    return False
