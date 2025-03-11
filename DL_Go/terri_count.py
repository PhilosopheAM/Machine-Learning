from collections import deque
from math import sqrt
from typing import List, Tuple, Set

from goboard_use import Board, GameState
from gotypes import *


class SimpleTerri:
    @staticmethod
    def go_stones_number(board:Board = None, gamestate:GameState = None) -> List[int]:
        """
        The most simple and silly way to determine the situation. Return the total number of black stones, white stones and neutral land.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :param gamestate: The parameter is a Gamestate object. Default set as None. If board param is not given, function will fetch the board attribute from gamestate and set it as local param board.

        :return: Always returns a list[3] of int. The first and second indicates how many black and white stones still stay on the board. The third int value is how many neutral land remains.
        """
        assert board is not None or gamestate is not None,"Lack of neccesary board info!"
        if gamestate is not None:
            board = gamestate.board
        else:
            pass
        board_column = board.num_cols
        board_row = board.num_rows
        black_stones_number, white_stones_number, neutral_number = 0, 0, 0
        for row in range(1, board_row + 1):
            for col in range(1, board_column + 1):
                bdg = board.get(Point(row, col))
                if bdg is None:
                    neutral_number += 1
                elif bdg == Player.black:
                    black_stones_number += 1
                else:
                    white_stones_number += 1
        return [black_stones_number, white_stones_number, neutral_number]

class ComplexTerri:

    class InfluenceInfoPackage:
        def __init__(self, influence_distance:int = 5, decay_constant:float = 0.6, multiply_constant:float = 1, default_score:float = 0.2, classify_line = 0.8):
            self.influence_distance = influence_distance
            self.decay_constant = decay_constant
            self.multiply_constant = multiply_constant
            self.default_score = default_score
            self.classify_line = classify_line

    @staticmethod
    def accurate_terri_number(board:Board = None, gamestate: GameState = None) -> List[int]:
        """
        Return the accurate value of land captured and neutral land remains without any estimation. It does not include liberty check, i.e. you should make sure GoString is always alive when checking land captured.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :param gamestate: The parameter is a Gamestate object. Default set as None. If board param is not given, function will fetch the board attribute from gamestate and set it as local param board.
        :return: Always returns a list[3] of int. The first and second indicates how many territories black and white player has respectively captured. The third int value is how many neutral land remains.
        """
        assert board is not None or gamestate is not None,"Lack of neccesary board info!"
        if gamestate is not None:
            board = gamestate.board
        else:
            pass
        # assert isinstance(board, Board), "The parameter must be a GoBoard object."
        board_set = ComplexTerri.accurate_terri_set(board)
        black_count = len(board_set[0])
        white_count = len(board_set[1])
        neutral_count = len(board_set[2])
        return [black_count, white_count, neutral_count]

    @staticmethod
    def accurate_terri_set(board:Board = None, gamestate: GameState = None) -> List[set[Point]]:
        """
        Use flood-fill algorithm to identify black and white land.
        Return three sets of points. The first set includes the points captured by black players. The second set includes the points captured by white players. The last set includes the points remained neutral.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :param gamestate: The parameter is a Gamestate object. Default set as None. If board param is not given, function will fetch the board attribute from gamestate and set it as local param board.
        :return: Always returns a list containing three sets. Sets contain the points captured by black players, white players, and remained neutral respectively.
        """
        # assert isinstance(board, Board), "The parameter must be a GoBoard object."
        assert board is not None or gamestate is not None,"Lack of neccesary board info!"
        if gamestate is not None:
            board = gamestate.board
        else:
            pass
        board_column, board_row = board.size()
        black_set = set() # Include territory and go
        white_set = set()# Include territory and go
        neutral_set = set()
        already_checked_points = set()

        # Sets that store go stones 
        black_go_set = set()
        white_go_set = set()

        # Use two steps to record the set. 
        # First we use _flood_fill to get region and border, analyze region situation. 
        # Then we literate the board to add go stones to set.

        # First Step
        for row in range(1, board_row + 1):
            for col in range(1, board_column + 1):
                current_point = Point(row, col)
                current_point_color = board.get(current_point)
                if current_point_color is not None:
                    if current_point_color == Player.black:
                        black_go_set.add(current_point)
                    elif current_point_color == Player.white:
                        white_go_set.add(current_point)
                    else:
                        pass # Should not enter there
                    continue
                elif current_point in already_checked_points:
                    continue
                else:
                    # See if the border is in the same color, using token 'border_in_one_color'
                    region, border = ComplexTerri.__flood_fill(current_point, board)
                    border_color_white = 0
                    border_color_black = 0
                    border_in_one_color = True
                    for border_point in border:
                        border_color_white += 1 if board.get(border_point) is Player.white else 0
                        border_color_black += 1 if board.get(border_point) is Player.black else 0
                        if border_color_white >= 1 and border_color_black >= 1: # Region is not surrounded by only one color stones
                            border_in_one_color = False
                            break
                        else:
                            pass # If all border_point in border is with the same color, the token would keep as unchanged True

                    # If the border is in the same color, we update the black or white set.
                    if border_in_one_color:
                        iter_obj = iter(border) # Transform border into an iterable object
                        color_of_border = board.get(next(iter_obj)) # next() in set will return an element but not delete it, compared to pop()
                        assert color_of_border == Player.black or color_of_border == Player.white, "Here's a problem with border color." # Theoretically, we won't use it at any time. But...
                        if color_of_border == Player.black:
                            black_set.update(region)
                            black_set.update(border)
                        else: # color should be white
                            white_set.update(region)
                            white_set.update(border)
                    else: # Region does not belong to any player
                        neutral_set.update(region)

                    # Update region and border to the visited set, since they have been checked in __flood_fill method
                    already_checked_points.update(region)
                    already_checked_points.update(border)
        # Second Step
        black_set.update(black_go_set)
        white_set.update(white_go_set)
        # Return a list including three set[Point]
        points_terri_result: List[set[Point]] = [black_set, white_set, neutral_set]
        return points_terri_result
    
    @staticmethod
    def estimated_terri_number(board:Board = None, gamestate: GameState = None, iip: InfluenceInfoPackage = InfluenceInfoPackage()) -> List[Set]:
        """
        Return the accurate value of land captured and neutral land remains with estimation. It does not include liberty check, i.e. you should make sure GoString is always alive when checking land captured.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :param gamestate: The parameter is a Gamestate object. Default set as None. If board param is not given, function will fetch the board attribute from gamestate and set it as local param board.
        :param iip: Including the information about influential model. When is none, use default InfluenceInfoPackage setting.
        :return: Always returns a list[3] of int. The first and second indicates how many territories black and white player has respectively captured. The third int value is how many neutral land remains.
        """
        assert board is not None or gamestate is not None,"Lack of neccesary board info!"
        if gamestate is not None:
            board = gamestate.board
        else:
            pass
        black_set, white_set, neutral_set = ComplexTerri.estimated_terri_set(board, iip=iip)
        return [len(black_set), len(white_set), len(neutral_set)]

    @staticmethod
    def estimated_terri_set(board:Board = None, gamestate: GameState = None, iip:InfluenceInfoPackage = None) -> Tuple[set[Point]]:
        """
        Return the estimated value of land captured and neutral land remains. It does not include liberty check, i.e. you should make sure GoString is always alive when checking land captured.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :param gamestate: The parameter is a Gamestate object. Default set as None. If board param is not given, function will fetch the board attribute from gamestate and set it as local param board.
        :param iip: Including the information about influential model. When is none, use default InfluenceInfoPackage setting.
        :return: Always returns a list containing three sets. Sets contain the points captured(or seems to have a great influence on) by black players, white players, and remained neutral respectively.
        """
        assert board is not None or gamestate is not None,"Lack of necessary board info!"
        if gamestate is not None:
            board = gamestate.board
        else:
            pass
        accurate_set_list = ComplexTerri.accurate_terri_set(board)
        black_set = accurate_set_list[0]  # Include territory and go
        white_set = accurate_set_list[1]  # Include territory and go
        neutral_set = accurate_set_list[2] # From neutral set, estimate potential territory by influence model

        # assert iip is not None and isinstance(iip, ComplexTerri.InfluenceInfoPackage),"Influence info package invalid! You'd better call this function through estimated_terri_number()!"
        # Influence model default parameters
        # influence_distance: int = iip.influence_distance
        # decay_constant:float = iip.decay_constant
        # multiply_constant:float = iip.multiply_constant
        # default_score:float = iip.default_score
        if iip is None:
            print("You'd better call this function through estimated_terri_number()!\n")
            print("We will use default InfluenceInfoPackage setting.")
            iip = ComplexTerri.InfluenceInfoPackage()
        classify_line:float = iip.classify_line
        
        # Check if a candidate point satisfies the condition.
        for candidate_point in neutral_set.copy(): # Use shallow copy to avoid set runtime error: Set changed during iteration
            current_score = ComplexTerri.__influence_weighting_calculator(candidate_point, board, iip)
            both_score_total = current_score[0] + current_score[1]
            if current_score[0]/both_score_total > classify_line:
                black_set.add(candidate_point)
                neutral_set.discard(candidate_point)
            elif current_score[1]/both_score_total > classify_line:
                white_set.add(candidate_point)
                neutral_set.discard(candidate_point)
            else:
                pass

        return black_set, white_set, neutral_set

    @staticmethod
    def __flood_fill(start: Point, board:Board) -> tuple[set[Point], set[Point]]:
        """Implementation of flood-fill algorithm. Check the region connected to the start point and the border of the region when the start point is neutral.
            Args:
                start: start point
            Returns:
                (region points, border points)
        """
        queue = deque([start]) # Build a queue list to maximize the data access efficiency at endpoints
        visited = set()
        region = set()
        border = set()


        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            if board.get(current) is None: # If the current point is empty
                region.add(current)
                for neighbor in current.neighbor_with_bound_constraint(constraint=board.size()):
                    if neighbor in visited:
                        continue
                    else:
                        queue.append(neighbor)
            else: # If the current point has been captured
                border.add(current)

        return region, border

    @staticmethod
    def __influence_weighting_calculator(target_point:Point, board:Board, iip: InfluenceInfoPackage) -> tuple[float, float]:
        """
        Use recursive method to get nearby points. With Euclidean distance set as exponential parameter, we design an exponential decay model to sum up the total effect comes from nearby points on a point.
        :param target_point: The point to be checked.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :return: Always returns a tuple including two floats. The first one is how much influence black stones give to this point. The second is how much influence white stones give to this point.
        """

        assert (isinstance(target_point, Point) and isinstance(board, Board)), "Point or Board invalid!"
        assert iip is not None and isinstance(iip, ComplexTerri.InfluenceInfoPackage), "Influence info package missed or invalid!"
        # Influence model default parameters
        influence_distance: int = iip.influence_distance
        decay_constant:float = iip.decay_constant
        multiply_constant:float = iip.multiply_constant
        black_score = iip.default_score
        white_score = iip.default_score # default score is 0.1
        queue = deque() # Initialization
        queue.append(target_point) # Initialization
        # queue.append(target_point)
        visited = set() # Points that have been checked
        # valid_points = set() # Points involve in calculating the score. Points whose distance from the target point is less than influence distance.

        while queue:
            current = queue.popleft()
            # print(current)
            current_coordinate = current.get()
            neighbors = set(current.neighbor_with_bound_constraint(constraint=board.size())) # Transform into set type to speed up
            for candidate_point in neighbors - visited: # Use the attribute of Set to speed up searching. Find points in candidate_point but not in visited.
                visited.add(candidate_point) # append current selected point to visited set
                neighbor_coordinate = candidate_point.get()
                distance_squared = (neighbor_coordinate[0] - current_coordinate[0])**2 + (neighbor_coordinate[1] - current_coordinate[1])**2
                if distance_squared <= influence_distance**2 and board.get(candidate_point) is not None: # candidate point is valid, should take into consideration
                    queue.append(candidate_point)
                    distance = sqrt(distance_squared)
                    score_influence = multiply_constant * (decay_constant**distance) # exponential decay sum up
                    if board.get(candidate_point) is Player.black:
                        black_score += score_influence
                    elif board.get(candidate_point) is Player.white:
                        white_score += score_influence
                    else:
                        raise TypeError("The candidate point is not black or white.") # Should not enter
                else:
                    pass
        return black_score, white_score

