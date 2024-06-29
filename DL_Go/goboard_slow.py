import copy
from gotypes import Player, Point

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
            (self.liberties | go_string.liberties) - merged_stones_set ## Here do union first, then do difference.  
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
    
class Board():
    def __init__(self, num_rows,num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {} ## _grid is a dict, we use 'get' method latter to get GoString class instance stored inside.

    def place_stone(self, player, point):
        assert self.is_on_grid(point) ## Make sure the coordinate given is usable
        assert self._grid.get(point) is None ## Make sure there is no stone in the place of the given coordinate of point
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor_stone in point.neighbors():
            if not self.is_on_grid(neighbor_stone):
                continue ## We use keyword 'continue' to escape from this round of iteration. 
            
            ## Only those neighbors with reachable coordinates will go into following steps
            neighbor_string = self._grid.get(neighbor_stone)
            if neighbor_string is None:
                liberties.append(neighbor_stone)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else: ## Here remains the only condition, the neighbor_string is not the same color as the player. We still need to check if the neighbor_string has already included in adjacent_opposite_color.
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string) 
        
        new_string = GoString(player, [point], liberties)
        ## Assemble the given GoString type instance with each of the adjacent GoString type



    def is_on_grid(self,point):
        return (1 <= point.row <= self.num_rows) and (1 <= point.col <= self.num_cols)

    def get(self, point):
        stone_string = self._grid.get(point)
        if stone_string is None:
            return None
        return stone_string.color ## 'color' is Player class
    
    def get_go_string(self,point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string
