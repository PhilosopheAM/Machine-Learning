import random
from .base import Agent
from .helpers import is_point_an_eye
import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from goboard_use import Move, GameState
from gotypes import Point

class RandomBot(Agent):
    def select_move(self, game_state:GameState) -> Move:
        # Random choice, valid moves. Very naive bot plays like a child.
        candidates = []
        for rv in range(1, game_state.board.num_rows + 1):
            for cv in range(1, game_state.board.num_cols + 1):
                location = Point(rv, cv)
                if game_state.is_valid_move(Move.play(location)) and not is_point_an_eye(game_state.board, location, game_state.next_player):
                    candidates.append(location)
        
        if not candidates: 
            return Move.pass_turn()

        return Move.play(random.choice(candidates))