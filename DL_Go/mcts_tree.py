import goboard_use
from DL_Go.zobrist_hashing_generator import state


class Node:
    """
    A node in the search tree.

    Attributes:
        state (GameState): The current state of the node.
        parent (Node): The parent node of the node.
        children (List[Node]): The children of the node.
        visits [int]: The number of times this node is visited.
        reward [float]: The reward of the node. In this implementation, it might be negative.
    """
    def __init__(self, state:goboard_use.GameState, parent = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

    def is_fully_expanded(self):
        return (len(self.children) == state.)



class MCTS: