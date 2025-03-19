import naive
import copy
from platform import node
from ..goboard_use import GameState, Board, Move
from ..gotypes import Point, Player
from ..terri_count import ComplexTerri, SimpleTerri
import math
from collections import namedtuple

''' Too messy. Need to rebuild all.
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
        self.expandable_moves = self.all_valid_moves
        # self.is_final_node = True if len(self.all_valid_moves) == 0 else False # No play available when true.
        self.children_moves = set() # Expanded children_moves nodes.

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
            current_score = i.reward/i.visits + uct_explor * math.sqrt(math.log(self.visits) / i.visits)
            if current_score > best_score_now:
                best_child_node = i
                best_score_now = current_score
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
    def reward_exponential_decay_normalization(result:list, player: Player, k:float) -> float :
        """
        Convert terri result into a normalization reward function (0~2). Use exponential decay method.
        Args:
            result: A list consists of black territory, white territory and neutral lands.
            player: The player places the next stone.
            k: decay parameter. Set 0.184 as default. With lager k, the reward would grow intensively.

        """
        assert isinstance(result,list) and len(result) == 3 and k > 0, "Illegal parameter!"
        black, white, neutral = result
        total_play = black + white
        total_terri = black + white + neutral # We use 19*19=361 as the baseline of total territory.
        




    
    def change_strategy(self, former:MCTS_Strategy = None, latter:MCTS_Strategy = None, divider:float = None) -> None:
        if former is not None:
            self.strategy_former_half = former
        if latter is not None:
            self.strategy_latter_half = latter
        if divider is not None:
            self.division_line = divider

    def get_best_move(self, state:GameState = None) -> Move:
        """
        Get the best move of the current gamestate based on MCTS strategy.
        Args:
            state: The game state to simulate.
        Returns:
            Move:A Move object represents the best move under the given condition.
        """
        strategy_use = self.strategy_former_half if (1-stone_list[2]/self.total_terri)<self.divider_line else self.strategy_latter_half

        # Resign check
        stone_list = SimpleTerri.go_stones_number(gamestate=state)
        if stone_list[0] + stone_list[1] < 5:
            pass
        else: # Enough steps to apply situation check. Determine whether it is better to resign rather than playing until the last stone is placed.
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

 '''       

'''
MCTS Structure
1. An agent call an api function -> The best move(Move object) under certain gamestate (resign, pass or play). The former two should be decided independently. The latter one(play) uses an individual simulation function.
2. The simulation function also called MCTS.
3. MCTS is an instance with two important parameter, running-step/time-limitation and strategy-package.
4. Strategy package includes:
    + uct formula exploration parameter
    + auto-resign enable sign
    + step interval for situation check while simulating
    + auto-resign divider line
'''
class Node4MCTS:
    def __init__(self, gamestate = GameState):
        self.gamestate = gamestate
        self.move = None # The move linked to this node. Applying this move to node's parent node, it will come to the current node.
        self.parent = None
        self.children = set() # Contains Node4MCTS objects that are the leaf nodes of the current node.
        self.visit = 0
        self.reward = 0

        # Additional attributes to asist node expand
        self.available_next_move = self.gamestate.get_all_valid_play_moves()
        self.moves_in_children = set()


class MCTS:
    """
    Implementation of MCTS in 19x19 go board.
    """
    def __init__(self):
        self.resign_divider_line = 0.9
        self.limit = Limitation4MCTS()
        self.strategy = Strategy4UCT()
        
    def set_resign_line(self, resign_line:float):
        assert resign_line > 0 and resign_line < 1, "Unvalid resign line."
        self.resign_divider_line = resign_line

    def set_strategy(self, strategy: Strategy4UCT): # type: ignore
        assert isinstance(strategy, Strategy4UCT)
        self.strategy = strategy
    def set_limit(self, limit: Limitation4MCTS): # type: ignore
        assert isinstance(limit, Limitation4MCTS)
        self.limit = limit

    def select_next_move(self, gamestate: GameState) -> Move:
        """
        Select the best move for the given game state.
        Args:
            gamestate: The current game state to evaluate.
        Returns:
            Move:A Move object represents the best move under the given condition.
        """
        # Pass check
        if len(gamestate.get_all_valid_play_moves()) < 1:
            return Move.pass_turn()
        # Resign check
        stone_list = SimpleTerri.go_stones_number(gamestate=gamestate)
        if stone_list[0] + stone_list[1] < 10:
            pass
        else: # Enough steps to apply situation check. Determine whether it is better to resign rather than playing until the last stone is placed.
            estimated_terri_list = ComplexTerri.estimated_terri_number(gamestate=gamestate)
            better_to_resign = False
            match gamestate.next_player:
                case Player.black:
                    better_to_resign = True if estimated_terri_list[1]/estimated_terri_list[0] >= self.resign_divider_line else False
                case Player.white:
                    better_to_resign = True if estimated_terri_list[0]/estimated_terri_list[1] >= self.resign_divider_line else False
                case _:
                    raise Exception("Illegal Player in mcts: get_best_move method!")
            if better_to_resign: 
                return Move.resign()
        # Select a play move
        root_node = Node4MCTS(gamestate)
        next_move = None # The return value
        if self.limit.time is not None and isinstance(self.limit.time, float) and self.limit.time > 0: # Priority 0
            pass
        elif self.limit.step is not None and isinstance(self.limit.step, int) and self.limit.step > 0: # Priority 1
            pass
        else:
            raise ValueError("Invalid time or step value")
        
        if next_move is not None:
            return next_move
        else:
            raise TypeError("Invalid return, expect a move.")
        
    def simulate_time(self, rootNode: Node4MCTS) -> Move:
        total_time = self.limit.time
        pass

    def simulate_step(self, rootNode: Node4MCTS) -> Move:
        pass

    def simulate_once(self, rootNode: Node4MCTS) -> None:
        resign_enable = self.strategy.auto_resign_enable
        # To save running time resources, use similiar but little different implementation

        last_node = None # The end of the simulation node
        leaf_node = None # The parent of the rootNode, should be None. Use to mark the end of the rewarding process
        if resign_enable:
            pass
        else:
            pass
    
    # TODO
    def select_leaf_node(self, rootNode: Node4MCTS) -> Node4MCTS:
        current_node = rootNode # The most suitable node in the current searching tree level

        while(len(current_node.children) > 0):
            

        return current_node



class Limitation4MCTS(namedtuple(typename='Limitation4MCTS',field_names=['time','step'])):
    """
    An object includes the information of the limitation for a MCTS running program. It includes two attributes: time and step. 'time' indicates how much time it goes before the program stops and 'step' limits the simulation times.
    Time is set 5 seconds as default. Step is set 2500 as default.
    """
    def __new__(cls, time=5, step=2500):
        instance = super(Limitation4MCTS, cls).__new__(cls, time, step)
        if not instance.valid_check():
            raise ValueError("Invalid time or step value")
        return instance
    
    def valid_check(self) -> bool:
        if self.time is not None and isinstance(self.time, float):
            return True
        elif self.step is not None and isinstance(self.step, int):
                return True
        else:
            return False
class Strategy4UCT(namedtuple(typename='Strategy4UCT', field_names=['uct_explor','auto_resign_enable','check_interval',"auto_resign_divider_line"])):
    """
    Strategy package contains the information used for MCTS. 'auto_resign_enable' will set False as default.'check_interal' and 'auto_resign_divider' will set 10 and 0.9 as default.
    """
    def __new__(cls, uct_explor = 1.414, auto_resign_enable = False, check_interval = 10, auto_resign_divider_line = 0.9):
        instance = super(Limitation4MCTS, cls).__new__(cls, uct_explor, auto_resign_enable, check_interval, auto_resign_divider_line)
        if not instance.valid_check():
            raise ValueError("Invalid time or step value")
        return instance
    
    def valid_check(self) -> bool:
        if self.uct_explor is None or not isinstance(self.uct_explor, float):
            return False
        if self.auto_resign_enable is False:
            return True
        else: # self.auto_resign_enable is True and should check following parameters
            if self.check_interval is None or not isinstance(self.check_interval, int) or self.check_interval < 0:
                return False
            if self.auto_resign_divider_line is None or not isinstance(self.auto_resign_divider_line,float) or self.auto_resign_divider_line <= 0 or self.auto_resign_divider_line > 1:
                return False
            return True


class Node:
    pass
        
        
        
