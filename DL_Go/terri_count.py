from pydantic.json import deque

from goboard_use import Board
from gotypes import *
from typing import List, Tuple, Set

class SimpleTerri:
    @staticmethod
    def go_stones_number(board:Board) -> List[3]:
        """
        The most simple and silly way to determine the situation. Return the total number of black stones, white stones and neutral land.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :return: Always returns a list[3] of int. The first and second indicates how many black and white stones still stay on the board. The third int value is how many neutral land remains.
        """
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
    @staticmethod
    def accurate_terri_number(board:Board) -> List[3]:
        """
        Return the accurate value of land captured and neutral land remains without any estimation. It does not include liberty check, i.e. you should make sure GoString is always alive when checking land captured.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :return: Always returns a list[3] of int. The first and second indicates how many territories black and white player has respectively captured. The third int value is how many neutral land remains.
        """
        assert isinstance(board, Board), "The parameter must be a GoBoard object."
        board_set = ComplexTerri.accurate_terri_set(board)
        black_count = len(board_set[0])
        white_count = len(board_set[1])
        neutral_count = len(board_set[2])
        return [black_count, white_count, neutral_count]

    @staticmethod
    def accurate_terri_set(board:Board) -> List[set[Point]]:
        """
        Use flood-fill algorithm to identify black and white land.
        Return three sets of points. The first set includes the points captured by black players. The second set includes the points captured by white players. The last set includes the points remained neutral.
        :param board: The parameter is a board object. It is the current go board that needs to be checked.
        :return: Always returns a list containing three sets. Sets contain the points captured by black players, white players, and remained neutral respectively.
        """
        assert isinstance(board, Board), "The parameter must be a GoBoard object."
        board_column, board_row = board.size()
        black_set = set() # Include territory and go
        white_set = set()# Include territory and go
        neutral_set = set()
        already_checked_points = set()

        # Use two steps to record the set. First we use _flood_fill to get region and border, analyze region situation. Then we literate the board to add go stones to set.
        for row in range(1, board_row + 1):
            for col in range(1, board_column + 1):
                current_point = Point(row, col)
                if board.get(Point(row, col)) is not None or current_point in already_checked_points:
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
                        color_of_border = board.get(border[0])
                        assert color_of_border == Player.black or color_of_border == Player.white, "Here's a problem with border color." # Theoretically, we won't use it at any time. But...
                        if color_of_border == Player.black:
                            black_set.add(region)
                            black_set.add(border)
                        else: # color should be white
                            white_set.add(region)
                            white_set.add(border)
                    else: # Region does not belong to any player
                        neutral_set.update(region)

                    # Update region and border to the visited set, since they have been checked in __flood_fill method
                    already_checked_points.update(region)
                    already_checked_points.update(border)

        # Return a list including three set[Point]
        points_terri_result: List[set[Point]] = [black_set, white_set, neutral_set]
        return points_terri_result

    @staticmethod
    def __flood_fill(start: Point, board:Board) -> tuple[set[Point], set[Point]]:
        """Implementation of flood-fill algorithm. Check the region connected to the start point and the border of the region when the start point is neutral.
            Args:
                start: start point
            Returns:
                (region points, border points)
        """
        queue = deque[start] # Build a queue list to maximize the data access efficiency at endpoints
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
                for neighbor in current.neighbor_with_bound_constraint(board.size()):
                    if neighbor in visited:
                        continue
                    else:
                        queue.append(neighbor)
            else: # If the current point has been captured
                border.add(current)

        return region, border

    @staticmethod
    def __influence_weighting_calculator(board:Board):
        pass
