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
        self.point = point
        self.is_play = (self.point is not None) ## Here the 'point is not None' is used as a simplified function to identify whether self.point is registered as None. It returns a boolean value which then transferred to self.is_play
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)