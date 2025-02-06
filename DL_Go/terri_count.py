from goboard_use import Board
import gotypes
from typing import List, Tuple, Set

def accurate_terri_number(board:Board) -> List[3]:
    """
    Return the accurate value of land captured and neutral land remains without any estimation. It does not include liberty check, i.e. you should make sure GoString is always alive when checking land captured.
    :param board: The parameter is a board object. It is the current go board that needs to be checked.
    :return: Always returns a list[3] of int. The first and second indicates how many territories black and white player has respectively captured. The third int value is how many neutral land remains.
    """
    board_set = accurate_terri_set(board)
    black_count = len(board_set[0])
    white_count = len(board_set[1])
    neutral_count = len(board_set[2])
    return [black_count, white_count, neutral_count]

def accurate_terri_set(board:Board) -> List[Set[gotypes.Point]]:
    """
    Return three sets of points. The first set includes the points captured by black players. The second set includes the points captured by white players. The last set includes the points remained neutral.
    :param board: The parameter is a board object. It is the current go board that needs to be checked.
    :return: Always returns a list containing three sets. Sets contain the points captured by black players, white players, and remained neutral respectively.
    """


