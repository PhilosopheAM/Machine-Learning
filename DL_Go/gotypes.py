from enum import Enum
from collections import namedtuple

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
        return[
            Point(self.row -1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1),
        ]