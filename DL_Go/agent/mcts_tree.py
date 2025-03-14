import naive
import copy
from platform import node
from ..goboard_use import GameState, Board, Move
from ..gotypes import Point, Player
from ..terri_count import ComplexTerri, SimpleTerri
import math


class Node:
    """
    A node in the search tree.

    Attributes:
        state (GameState): The current state of the node.
        parent (Node): The parent node of the node.
        expand_children (Set[Node]): Expanded children_moves nodes.
        visits [int]: The number of times this node is visited.
        reward [float]: The reward of the node. In this implementation, it might be negative.
        is_final_node(bool): No play available when true.
        is_expanded(bool): Whether any of its children_moves node has been checked
        all_valid_moves(set[Point]): All legal children_moves play points.
    """
    def __init__(self, state:GameState, parent = None):
        self.state = state
        self.move = None
        self.parent = parent
        self.visits = 0
        self.reward = 0
        self.children_nodes = set()

        self.all_valid_moves = state.get_all_valid_play_moves()
        # self.is_final_node = True if len(self.all_valid_moves) == 0 else False # No play available when true.
        self.children_moves = set() # Expanded children_moves nodes.
        self.expandable_moves = self.all_valid_moves

    def is_fully_expanded(self):
        if self.expandable_moves > 0:
            return False
        elif self.expandable_moves == 0:
            return True
        else:
            raise Exception("Check Node. Illegal expanding condition.")
    
    def have_been_expanded(self):
        return len(self.children_nodes) > 0
    
    def select_child_node(self, uct_explor:float = 1.414):
        
        # # If the parent node has not been expanded fully, choose an available child node randomly
        # if not self.is_fully_expanded():
        #     return self.expand_new_node()
        
        # If the parent node has been fully expanded, use uct formula to decide which route to explore
        best_child_node = None
        best_score_now = float('-inf')
        for i in self.children_nodes:
            if (i.reward/i.visits + uct_explor * math.sqrt(math.log(self.visits) / i.visits)) > best_score_now:
                best_child_node = i
        return best_child_node
    
    def update_result(self):
        pass
    
    def expand_new_node(self):
        assert self.is_fully_expanded is False, "Node has been fully expanded, no more valid children node."
        new_move = self.expandable_moves.pop()
        self.children_moves.add(new_move)
        this_new_node = Node(self.state.apply_move(new_move), parent=self)
        this_new_node.move = new_move
        self.children_nodes.add(this_new_node)
        return this_new_node
    
    def run_one_time(self, uct_explor:float = 1.414, check_time:int = None, iip:ComplexTerri.InfluenceInfoPackage = ComplexTerri.InfluenceInfoPackage(), resign_line:float = 0.9):
        """
        To simulate the game once. If param check_time is not None, provide extra auto-resign function.
        Args:
            uct_explor: The exploration parameter for uct formula. The greater, the more likely to choose an unexplored route.
            check_time: The interval between auto-resign check. Set as None in default. To enable this function, you have to set it as a positive integer.
            iip: Param package for territory estimation function.
            resign_line: When to resign. = opponent's terri / self terri
        """
        # Initializing. The origin to start simulation
        leaf_explore = self
        while leaf_explore.is_fully_expanded():
            leaf_explore = leaf_explore.select_child_node(self,uct_explor)
        leaf_explore = leaf_explore.expand_new_node()

        auto_resign_enabled = True if (check_time is not None and isinstance(check_time, int) and check_time > 0) else False
        pass
    
    def simulate_with_auto_resign(self, iip:ComplexTerri.InfluenceInfoPackage = ComplexTerri.InfluenceInfoPackage(), resign_line:float = 0.9):
        pass
    def simulate(self):
        game = copy.deepcopy(self.state) # Start gamestate
        bot = naive.RandomBot()
        while not game.is_over():
            mv = bot.select_move(game)
            game = game.apply_move(mv)
        return ComplexTerri.accurate_terri_number(game)






        



class MCTS:
    """
    Implementation of the MCTS algorithm.
    """
    class MCTS_Strategy:
        def __init__(self, running_cons:int = 5000, time_cons:float = 3, uct_explor:float = 1.414,  iip:ComplexTerri.InfluenceInfoPackage = None, resign_line:float = 0.9):
            self.running_cons = running_cons # How many times MCTS comes to an end
            self.time_cons = time_cons # How much time MCTS uses to get one decision
            self.utc_c = uct_explor # exploration parameter of Upper Confidence Bound formula
            self.iip = iip if isinstance(iip, ComplexTerri.InfluenceInfoPackage) else ComplexTerri.InfluenceInfoPackage() # If iip param is None, use default setting to build up an instance.
            self.resign_line = resign_line # When to resign. = opponent's terri / self terri

    def __init__(self, board_x:int = 19, board_y:int = 19):
        self.strategy_former_half = MCTS.MCTS_Strategy() # Use two different strategies in default to optimize the intelligence.
        self.strategy_latter_half = MCTS.MCTS_Strategy() 
        self.divider_line = 0.4 # When to switch strategy mode. = 1-neutral_left/board_total
        self.board_size_x = board_x # row
        self.board_size_y = board_y # column
        self.total_terri = self.board_size_x * self.board_size_y
    
    @staticmethod
    def exponential_decay_normalization(result:list, k:float, total_terri:int = 19*19):
        """
        Convert terri result into a normalization reward function (0~2). Use exponential decay method.
        """
        assert isinstance(result,list) and len(result) == 3 and k > 0, "Illegal parameter!"



    
    def change_strategy(self, former:MCTS_Strategy = None, latter:MCTS_Strategy = None, divider:float = None) -> None:
        if former is not None:
            self.strategy_former_half = former
        if latter is not None:
            self.strategy_latter_half = latter
        if divider is not None:
            self.division_line = divider

    def get_best_move(self, state:GameState = None) -> Move:
        strategy_use = self.strategy_former_half if (1-stone_list[2]/self.total_terri)<self.divider_line else self.strategy_latter_half

        # Resign check
        stone_list = SimpleTerri.go_stones_number(gamestate=state)
        if stone_list[0] + stone_list[1] < 5:
            pass
        else: # Enough steps to apply situation check
            estimated_terri_list = ComplexTerri.estimated_terri_number(gamestate=state, iip=strategy_use.iip)
            better_to_resign = False
            match state.next_player:
                case Player.black:
                    better_to_resign = True if estimated_terri_list[1]/estimated_terri_list[0] >= strategy_use.resign_line else False
                case Player.white:
                    better_to_resign = True if estimated_terri_list[0]/estimated_terri_list[1] >= strategy_use.resign_line else False
                case _:
                    raise Exception("Illegal Player in mcts: get_best_move method!")
            if better_to_resign:
                return Move.resign()
            
        root = Node(state)
        # Pass check
        if len(state.get_all_valid_play_moves()) < 1:
            return Move.pass_turn()

        # Play, select the best next move

        


        
        
        
        
