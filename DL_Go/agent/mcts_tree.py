from ..goboard_use import GameState, Board, Move
from ..gotypes import Point, Player

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
        is_expanded(bool): Whether any of its childre node has been checked
        all_valid_children(set[Point]): All legal children play points.
    """
    def __init__(self, state:GameState, parent = None):
        state = state
        parent = parent
        self.expand_children = set() # Expanded children nodes.
        self.visits = 0
        self.reward = 0
        self.is_final_node = False # No play available when true.
        self.is_expanded = False # Whether any of its childre node has been checked
        self.all_valid_children = state.get_all_valid_play_moves()
        if self.all_valid_children is None:
            self.is_final_node = True

    def is_fully_expanded(self):
        return (len(self.children) == state.)



class MCTS: