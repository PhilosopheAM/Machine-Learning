"""
Go board coordinates can be specified in many ways, but in Europe it's most common
to label the columns with letters of the alphabet, starting with A, and the rows with
increasing numbers, starting at 1. In these coordinates, on a standard 19 x 19 board, the
lower left corner would be A1, and the topright corner T19. Note that by convention
the letter I is omitted to avoid confusion with 1.
"""

import DL_Go.gotypes as gotypes

COLS = 'A B C D E F G H J K L M N O P Q R S T' # No 'I' since it might get confused like '1'
COLS_NO_SEP = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None:'\uFF0B',
    gotypes.Player.black : '\u26AB',
    gotypes.Player.white:'\u26AA'
}

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' %(COLS[2*(move.point.col - 1)], move.point.row)
    print('%s %s' %(player, move_str))

def print_board(board):
    for row in range(board.num_rows, 0, -1):
        bump = "  " if row <= 9 else " " # Make it looks good
        per_line = []
        for col in range(1, board.num_cols + 1):
            stone = board.get(gotypes.Point(row, col))
            per_line.append(STONE_TO_CHAR[stone])
        print('%s%d %s' %(bump, row, ''.join(per_line))) #''.join indicates that there is no seperator
    print('    '+''.join(COLS[:(2*board.num_cols)]))

