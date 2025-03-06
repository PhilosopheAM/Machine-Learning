from agent import naive
import goboard_use
import gotypes
from utils import print_board, print_move, print_accurate_condition
import time

def test_remove_function():
    # Use a small board to test. 5-5 BOARD.
    board_size = 19
    game = goboard_use.GameState.new_game(board_size)
    bot = naive.RandomBot()

    while not game.is_over():
        mv = bot.select_move(game)
        game = place_and_print(game, move = mv )
        string = game.board.get_go_string(mv.point)
        print('Target string has %d liberty.'%(len(string.liberties)))
        print()

    # game = place_and_print(game,(1,1))
    # game = place_and_print(game,(1,2))
    # game = place_and_print(game,(2,2))
    # game = place_and_print(game,(5,5))
    # game = place_and_print(game,(3,1))
    # game = place_and_print(game,(5,4))
    # game = place_and_print(game,(4,5))
    # game = place_and_print(game,(2,1))
    # game = place_and_print(game,(1,4))
    # game = place_and_print(game,(1,1))
    # game = place_and_print(game,(1,3))
    
    # game = place_and_print(game,(1,1))

    '''

    white = gotypes.Player.white
    black = gotypes.Player.black

    for i in range(1,4):
        for m in range(1,6):
            game = place_and_print(game, (i,m),player=black)
    for i in range(5,3,-1):
        for m in range(1,6):
            if (i,m) == (4,5):
                print()
            game = place_and_print(game, (i,m),player=white)
            if (i,m) == (4,5):
                print()
    '''

    



    # #test
    # p = gotypes.Point(1,1)
    # string = game.board.get_go_string(p)
    # for stone in string.liberties:
    #     print(str(stone) +'\n')


def place_and_print(game: goboard_use.GameState, point: tuple = None, move: goboard_use.Move = None, player:gotypes.Player = None) -> goboard_use.GameState:
    # time.sleep(2)
    # Check if some parameteres available
    if point is not None:
        point_now = gotypes.Point(point[0], point[1])
        move = goboard_use.Move.play(point_now)
    elif move is None:
        raise ValueError("Either 'point' or 'move' must be provided")
    
    if player is None:
        player = game.next_player
    else:pass

    print(chr(27) + "[2J")
    # clear_and_print(game)
    print_board(game.board)
    print_move(player, move)
    game = game.apply_move_designated_player(move,player)
    print('-----------------After Move----------------\n')
    print_board(game.board)
    return game

def clear_and_print(game: goboard_use.GameState):
    print(chr(27) + "[2J")
    print_board(game.board)

if __name__ == '__main__':
    test_remove_function()