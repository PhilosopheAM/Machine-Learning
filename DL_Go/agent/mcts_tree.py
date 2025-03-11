from ..goboard_use import GameState, Board, Move
from ..gotypes import Point, Player
from ..terri_count import ComplexTerri


class Node:
    """
    A node in the search tree.

    Attributes:
        state (GameState): The current state of the node.
        parent (Node): The parent node of the node.
        expand_children (Set[Node]): Expanded children nodes.
        visits [int]: The number of times this node is visited.
        reward [float]: The reward of the node. In this implementation, it might be negative.
        is_final_node(bool): No play available when true.
        is_expanded(bool): Whether any of its children node has been checked
        all_valid_children(set[Point]): All legal children play points.
    """
    def __init__(self, state:GameState, parent = None):
        state = state
        parent = parent
        self.expand_children = set() # Expanded children nodes.
        self.visits = 0
        self.reward = 0
        self.is_final_node = False # No play available when true.
        self.is_expanded = False # Whether any of its children node has been checked
        self.all_valid_children = state.get_all_valid_play_moves()
        if self.all_valid_children is None:
            self.is_final_node = True

    def is_fully_expanded(self):
        return len(self.expand_children) == len(self.all_valid_children)



class MCTS:
    """
    Implementation of the MCTS algorithm.
    """
    class MCTS_Strategy:
        def __init__(self, running_cons:int = 5000, time_cons:float = 3, iip:ComplexTerri.InfluenceInfoPackage = None):
            self.running_cons = running_cons
            self.time_cons = time_cons
            self.iip = iip