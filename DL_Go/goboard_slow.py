import copy
from .gotypes import Player, Point

'''
We following American Go Association(AGA)'s notation. At each round, a player should conduct a 'move'. A 'move' can be the following three actions:
1. Pass. Stop doing anything in this round and let the opponent do something.
2. Resign. Make it courteous when the player finds it hard to win.
3. Play. 'Play' means place a stone on the board.

Normally, most of the cases in a progressing game should be the third one, 'Play'. 
'''

class Move:
    def __init__(self, point = None, is_pass = False, is_resign = False):
        assert (point is not None) ^ (is_pass) ^ (is_resign)
        # The assertion makes sure each instance has only one target moving among 'play(allocate a point)', 'pass' or 'resign'. Or it will give out an error.
        self.point = point
        self.is_play = (self.point is not None) # Here the 'point is not None' is used as a simplified function to identify whether self.point is registered as None. It returns a boolean value which then transferred to self.is_play
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)
    # Use @classmethod decorator to use the function 'play' in class level. The first parameter 'cls' stands for class

    @classmethod
    def pass_turn(cls):
        return Move(is_pass= True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign= True)

'''
We call a group of connected stones of the same color a string of stones, or simply a string
'''
class GoString:
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

        # The following operations in this function are based on the property of the datatype Set
        merged_stones_set = self.stones | go_string.stones
        return GoString(
            self.color,
            merged_stones_set,
            (self.liberties | go_string.liberties) - merged_stones_set # Here do union first, then do difference.  
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
    
class Board:
    def __init__(self, num_rows,num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {} # _grid is a dict, we use 'get' method latter to get GoString class instance stored inside.

    def place_stone(self, player, point):
        assert self.is_on_grid(point) # Make sure the coordinate given is usable
        assert self._grid.get(point) is None # Make sure there is no stone in the place of the given coordinate of point
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor_stone in point.neighbors():
            if not self.is_on_grid(neighbor_stone):
                continue # We use keyword 'continue' to escape from this round of iteration. 
            
            # Only those neighbors with reachable coordinates will go into following steps
            neighbor_string = self._grid.get(neighbor_stone)
            if neighbor_string is None:
                liberties.append(neighbor_stone)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else: # Here remains the only condition, the neighbor_string is not the same color as the player. We still need to check if the neighbor_string has already included in adjacent_opposite_color.
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string) 
        
        new_string = GoString(player, [point], liberties)
        # Assemble the given GoString type instance with each of the same color adjacent (unique) GoString type
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string # Build the new key-value relation, i.e. the coordinate of the new-established go-string and the pointer of this string. It's a multi-key to one value mapping. 
        
        # Reduction of liberty of the adjacent opposite-color strings. (Remind uself of the difference of the adjacent stones and the adjacent strings)
        for opposite_color_string in adjacent_opposite_color:
            opposite_color_string.remove_liberty(point)
            if opposite_color_string.num_liberties == 0:
                self._remove_string(opposite_color_string)



    def is_on_grid(self,point):
        return (1 <= point.row <= self.num_rows) and (1 <= point.col <= self.num_cols)

    def get(self, point):
        stone_string = self._grid.get(point)
        if stone_string is None:
            return None
        return stone_string.color # 'color' is Player class
    
    def get_go_string(self,point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string

    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
                self._grid[point] = None


'''
Now we are going to implement a class named GameState. This class will allow us to know about the board position, the next player, the former(previous-move) game state and the recent move.
'''
class GameState:
    def __init__(self,board,next_player,previous_gamestate,this_move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_gamestate
        self.last_move = this_move

    def apply_move(self,move):
        if move.is_play:
            board_after_move = copy.deepcopy(self.board)
            board_after_move.place_stone(self.next_player,move.point)
        else:
            board_after_move = self.board
        return GameState(board_after_move,self.next_player.other,self,move)

    @classmethod
    def new_game(cls, board_size):
        assert isinstance(board_size,int), "Error: the board size should be int type or the board can not be created"
        board = Board(board_size,board_size)
        return GameState(board, Player.black,None, None)
    
    def is_over(self):

        # Surrender 
        if self.last_move.is_resign:
            return True
        # The first move of the game
        if self.last_move is None:
            return False
        
        former_second_move = self.previous_state.last_move
        if former_second_move is None:
            return False
        return self.last_move.is_pass and former_second_move.is_pass

    # Next we will check if a move leads to self-capture
    def is_move_self_capture(self, player, move):
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player,move.point)
        target_string_in_next_board = next_board.get_go_string(move.point)
        return target_string_in_next_board.num_liberties == 0

    @property
    def situation(self):
        return (self.next_player, self.board)
    
    # The following implementation of checking whether the moving operation violates 'ko' rule. It is obvious that it is too slow and costly. 
    # There is another method to speed up the checking using hashing code. In chess engine, we use Zobrsit hashing. I will implement it later and make the present one depreciated.
    def does_move_violate_ko(self, player,move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        checking_past_state = self.previous_state
        while checking_past_state is not None:
            if checking_past_state.situation == next_situation:
                return True
            checking_past_state = checking_past_state.previous_state
        return False

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        
        # When checking a 'Play' move, you need to make sure that: 1) the point given is legal 2) no self-capture 3) no violating ko rule
        play_move_checking = (self.board.get(move.point) is None) and \
                             (not self.is_move_self_capture(self.next_player,move)) and \
                             (not self.does_move_violate_ko(self.next_player, move))
        return play_move_checking
    