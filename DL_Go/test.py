from agent import naive
import goboard_use
import gotypes
from utils import print_board, print_move, print_accurate_condition
import time

def test_remove_function():
    # Use a small board to test. 5-5 BOARD.
    board_size = 5
    game = goboard_use.GameState.new_game(board_size)
    bot = naive.RandomBot()

    # while not game.is_over():
        # time.sleep(0.5)

        # """
        # 这行代码 `print(chr(27) + "[2J")` 是用来清除终端屏幕的。让我们分解一下这行代码的组成部分 :

        # 1. `chr(27)` :这是Python中的一个函数 ,`chr()` 函数返回对应ASCII码的字符。27 是 ASCII 码表中代表“转义字符(Escape)”的数字 ,所以 `chr(27)` 会返回一个转义字符(`\x1b`)。

        # 2. `"[2J"` :这是一个 ANSI 转义序列 ,用来清除屏幕。它告诉终端清除屏幕上的所有内容。

        # 所以 ,这行代码组合在一起的作用是发送一个 ANSI 转义序列给终端 ,要求它清除屏幕上的所有内容。这个功能在命令行界面中非常有用 ,可以让程序输出更清晰。

        # 总结一下 ,`print(chr(27) + "[2J")` 在终端中执行时会清除当前屏幕上的所有文本。
        # """
        # bot_move = bot.select_move(game)
        # game = place_and_print(game, move=bot_move)
        # # print_accurate_condition(game.board)

    # move1 = goboard_use.Move.play(gotypes.Point(2,2))
    # clear_and_print(game)
    # print_move(game.next_player, move1)
    # game = game.apply_move(move1)
    # print('-----------------After Move----------------\n')
    # print_board(game.board)
    game = place_and_print(game,(1,1))
    game = place_and_print(game,(1,2))
    game = place_and_print(game,(1,3))
    game = place_and_print(game,(1,4))
    game = place_and_print(game,(1,5))
    game = place_and_print(game,(2,1))
    game = place_and_print(game,(2,4))
    game = place_and_print(game,(5,2))
    game = place_and_print(game,(5,1))
    game = place_and_print(game,(2,3))
    game = place_and_print(game,(5,3))
    game = place_and_print(game,(1,4))
    game = place_and_print(game,(4,1))
    game = place_and_print(game,(2,5))
    game = place_and_print(game,(4,2))
    game = place_and_print(game,(3,4))
    # game = place_and_print(game,(2,4))
    string = game.board.get_go_string(gotypes.Point(2,4))
    print('Target string has %d liberty.'%(len(string.liberties)))



    # #test
    # p = gotypes.Point(1,1)
    # string = game.board.get_go_string(p)
    # for stone in string.liberties:
    #     print(str(stone) +'\n')


def place_and_print(game: goboard_use.GameState, point: tuple = None, move: goboard_use.Move = None) -> goboard_use.GameState:
    # Check if some parameteres available
    if point is not None:
        point_now = gotypes.Point(point[0], point[1])
        move = goboard_use.Move.play(point_now)
    elif move is None:
        raise ValueError("Either 'point' or 'move' must be provided")

    print(chr(27) + "[2J")
    # clear_and_print(game)
    print_board(game.board)
    print_move(game.next_player, move)
    game = game.apply_move(move)
    print('-----------------After Move----------------\n')
    print_board(game.board)
    return game

def clear_and_print(game: goboard_use.GameState):
    print(chr(27) + "[2J")
    print_board(game.board)

if __name__ == '__main__':
    test_remove_function()