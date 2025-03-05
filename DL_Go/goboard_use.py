import copy
from gotypes import Player, Point
import zobrist_hashing_content
from typing import Optional
from typing import List, Tuple

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
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)

    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)
        
    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    def merged_with(self, go_string):
        assert go_string.color == self.color , "Stone Color Unmatch"

        # The following operations in this function are based on the property of the datatype Set
        merged_stones_set = self.stones | go_string.stones
        return GoString(
            self.color,
            merged_stones_set,
            (self.liberties | go_string.liberties) - merged_stones_set  # Here do union first, then do difference.
        )

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
        self._grid = {} # _grid is a dict, we use 'get' method later to get GoString class instance stored inside.
        self.__hash = zobrist_hashing_content.EMPTY_BOARD

    def size(self) -> List[int]:
        """
        :return: A list with two integers representing the size of the board, i.e. the row and column.
        """
        return [self.num_rows, self.num_cols]
    def valid_play_check(self, player:Player, point:Point) -> bool:
        """
        Use this method to check if a play operation is valid or not. 
        Args:
            player: A Player object, who plays the next round.
            point: Where to place the stone.
        Returns:
            bool: If valid -> true, vice versa.
        """
        assert self.is_on_grid(point) # Make sure the coordinate given is usable
        assert self._grid.get(point) is None # Make sure there is no stone in the place of the given coordinate of point
        valid_neighbors = point.neighbor_with_bound_constraint(self.size())

        # Easy check first, to save runtime cost
        for check_n in valid_neighbors:
            if self.get_go_string() is None: return True
        
        # Further check, need more memory space
        valid_or_not = True
        temporary_board = copy.deepcopy(self)
        temporary_board.place_stone(player, point)
        tempo_string = temporary_board.get_go_string(point)
        if len(tempo_string.liberties):
            pass
        else:
            valid_or_not = False
        return valid_or_not
    def place_stone(self, player:Player, point:Point):
        # assert self.is_on_grid(point) # Make sure the coordinate given is usable
        # assert self._grid.get(point) is None # Make sure there is no stone in the place of the given coordinate of point
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        print('%s player places stone in (%d, %d)'%(player, point.row, point.col))
        valid_neighbors = point.neighbor_with_bound_constraint(self.size())
        for i in valid_neighbors:
            print('Neighbor: (%d, %d)\n'%(i.get()[0], i.get()[1]))
        for neighbor_stone in valid_neighbors:
            # if not self.is_on_grid(neighbor_stone):
            #     continue # We use keyword 'continue' to escape from this round of iteration. 

            # Only those neighbors with reachable coordinates will go into following steps
            neighbor_string = self._grid.get(neighbor_stone)
            if neighbor_string is None: # Empty, not have been captured
                liberties.append(neighbor_stone)
                print('(%d, %d) is empty.\n'%(neighbor_stone.row, neighbor_stone.col))
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
                    print('(%d, %d) is %s.\n'%( neighbor_stone.row, neighbor_stone.col, player))
            else: # Here remains the only condition, the neighbor_string is not the same color as the player. We still need to check if the neighbor_string has already included in adjacent_opposite_color.
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string) 
                    print('(%d, %d) is %s.\n'%(neighbor_stone.row, neighbor_stone.col, player.other))

        
        new_string = GoString(player, [point], liberties)
        # Assemble the given GoString type instance with each of the same color adjacent (unique) GoString type
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string # Build the new key-value relation, i.e. the coordinate of the new-established go-string and the pointer of this string. It's a multi-key to one value mapping. 
        
        self.__hash ^= zobrist_hashing_content.HASH_CODE[point, player]

        # Reduction of liberty of the adjacent opposite-color strings. (Remind uself of the difference of the adjacent stones and the adjacent strings)
        for opposite_color_string in adjacent_opposite_color:
            replacement = opposite_color_string.without_liberty(point)
            print(len(replacement.liberties))
            if replacement.num_liberties(): # The boolean function identifies whether 'replacement.num_liberties' is 0. If not, return True.
                self._replace_string(replacement)
            else:
                self._remove_string(opposite_color_string)


    def is_on_grid(self,point):
        return (1 <= point.row <= self.num_rows) and (1 <= point.col <= self.num_cols)

    def get(self, point) -> Optional[Player]: # Use typing.Optional to check the return value. It should be a Player object, but None is ok.
        """
        Check the stone color of the given point.

        Args:
            point: The given Point instance need to be processed.

        Returns:
            None: If the given place has not been captured by a stone.
            Player: A Player instance, expressed as a color.
        """
        stone_string = self._grid.get(point)
        if stone_string is None:
            return None
        else:
            return stone_string.color  # 'color' is Player class
    
    def get_go_string(self, point):
        string = self._grid.get(point)
        return string
    
    def _replace_string(self, new_string):
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string:GoString):
        for point in string.stones:
            gostring_visited = [] # User set type to check if the new item is the same with the existed
            # for neighbor in point.neighbors():
            #     neighbor_string = self._grid.get(neighbor)
            #     if neighbor_string is None:
            #         pass
            #     else:
            #         # gostring_visited.add(neighbor_string)
            #         gostring_visited.append(neighbor_string)
            for neighbor in point.neighbor_with_bound_constraint(self.size()):
                n_string = self._grid.get(neighbor)
                if n_string not in gostring_visited and n_string is not None:
                    gostring_visited.append(n_string)
            while gostring_visited:
                current_neighbor_string = gostring_visited.pop()
                self._replace_string(current_neighbor_string.with_liberty(point))
            self._grid[point] = None
            self.__hash ^= zobrist_hashing_content.HASH_CODE[point, string.color]

    def zobrist_hash(self):
        return self.__hash


'''
Now we are going to implement a class named GameState. This class will allow us to know about the board position, the next player, the former(previous-move) game state and the recent move.
'''
class GameState():
    def __init__(self,board,next_player,previous_gamestate,this_move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous_gamestate
        self.last_move = this_move
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(previous_gamestate.previous_states | {(previous_gamestate.next_player , previous_gamestate.board.zobrist_hash())})

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
        # The first move of the game
        if self.last_move is None:
            return False
        # Surrender 
        if self.last_move.is_resign:
            return True
        
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
    
    # The better implementation of ko rule identification
    def does_move_violate_ko(self, player,move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player,move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states
        # If 'next_situation' tuple already exists in 'self.previous_states' set, it will return 1 (yes), which indicates that the ko rule is violated.


    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        
        # When checking a 'Play' move, you need to make sure that:
        # 1) the point given is legal
        # 2) no self-capture
        # 3) no violating ko rule
        play_move_checking = (self.board.get(move.point) is None) and \
                             (not self.is_move_self_capture(self.next_player,move)) and \
                             (not self.does_move_violate_ko(self.next_player, move))
        return play_move_checking

    def get_valid_moves(self):
        valid_moves_list = []
        for column in range(1, self.board.num_rows + 1):
            for row in range(1, self.board.num_columns + 1):
                temp_move = Move.play(Point(row, column))
                if self.is_valid_move(temp_move):
                    valid_moves_list.append(temp_move)
        
        if len(valid_moves_list) == 0:
            return None
        else:
            return valid_moves_list