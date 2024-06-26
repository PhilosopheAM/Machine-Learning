import copy
from gotypes import Player

'''
We following American Go Association(AGA)'s notation. At each round, a player should conduct a 'move'. A 'move' can be the following three actions:
1. Pass. Stop doing anything in this round and let the opponent do something.
2. Resign. Make it courteous when the player finds it hard to win.
3. Play. 'Play' means place a stone on the board.

Normally, most of the cases in a progressing game should be the third one, 'Play'. 
'''

class Move():
    def __init__(self, point = None, is_pass = False, is_resign = False):
        assert (point is not None) ^ (is_pass) ^ (is_resign)
        ## The assertion makes sure each instance has only one target moving among 'play(allocate a point)', 'pass' or 'resign'. Or it will give out an error.
        self.point = point
        self.is_play = (self.point is not None) ## Here the 'point is not None' is used as a simplified function to identify whether self.point is registered as None. It returns a boolean value which then transferred to self.is_play
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)
    ## Use @classmethod decorator to use the fuction 'play' in class level. The first parameter 'cls' stands for class

    @classmethod
    def pass_turn(cls):
        return Move(is_pass= True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign= True)

'''
We call a group of connected stones of the same color a string of stones, or simply a string
'''
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self,point):
        self.liberties.add(point)

    def merged_with(self,go_string):
        assert go_string.color == self.color , "Stone Color Unmatch"

        ## The following operations in this fuction are based on the property of the datatype Set
        merged_stones_set = self.stones | go_string.stones
        return GoString(
            self.color,
            merged_stones_set,
            (self.liberties | go_string.liberties) - merged_stones_set
        )
    
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self,other):
        return (isinstance(other, GoString) and \
                self.color == other.color and \
                self.stones == other.stones and \
                self.liberties == other.liberties        
                )