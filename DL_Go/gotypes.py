from enum import Enum
from collections import namedtuple
from typing import List, Tuple

class Player(Enum):
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white
    
class Point(namedtuple('Point',['row','col'])):
    ## A namedtuple lets you access the coordinates as point.row and point.col instead
    ## of point[0] and point[1], which makes for much better readability.
    def neighbors(self):
        """
        Returns a list of the neighboring points, with no boarder detection. It might return point that is out of bounds.
        :return: A list of the neighboring points
        """
        return[
            Point(self.row -1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]

    def neighbor_with_bound_constraint(self, constraint:List[int, int])-> List:
        """
                Returns a list of the neighboring points, with boarder detection.
                :param constraint: Must be a list of two ints, (row, col).
                :return: A list of valid neighboring points. If the board is 1x1, it will return an empty list.
                """
        assert isinstance(constraint, list) and len(constraint) == 2, "The parameter constraint must be a list of two ints, (row, col)."
        assert all(isinstance(x, int) for x in constraint) and all((x>0) for x in constraint), "The row and column constraints must be positive integers."
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = self.row + dr, self.col + dc
            if 1 <= nr <= constraint[0] and 1 <= nc <= constraint[1]:
                neighbors.append(Point(nr, nc))
        return neighbors
