class Agent:
    def __init__(self) -> None:
        pass

    def select_move(self, game_state):
        raise NotImplementedError() # With raising this error, you ask the child functions to implement this function. The ancestor function (here) declares a requirement.