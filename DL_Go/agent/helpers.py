import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gotypes import Point

def is_point_an_eye(board, point, color):
    """
    Warning: Player should never place a stone on a real eye since this step is useless, compared to a peseudo eye.
    """
    if board.get(point) is not None:
        return False
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False
            
    friendly_corners_quantity = 0
    out_of_board_corner_quantity = 0

    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners_quantity += 1
        else:
            out_of_board_corner_quantity += 1
    
    if out_of_board_corner_quantity > 0:
        return friendly_corners_quantity + out_of_board_corner_quantity == 4

    return friendly_corners_quantity >= 3