from DL_Go.agent import naive
from DL_Go import goboard_use
from DL_Go import gotypes
from DL_Go.utils import print_board, print_move
import time

def main():
    # Use a small board to test. 9 - 9 BOARD.
    board_size = 9
    game = goboard_use.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: naive.RandomBot(),
        gotypes.Player.white: naive.RandomBot(),
    }

    while not game.is_over():
        time.sleep(0.3)

        """
        这行代码 `print(chr(27) + "[2J")` 是用来清除终端屏幕的。让我们分解一下这行代码的组成部分 :

        1. `chr(27)` :这是Python中的一个函数 ,`chr()` 函数返回对应ASCII码的字符。27 是 ASCII 码表中代表“转义字符(Escape)”的数字 ,所以 `chr(27)` 会返回一个转义字符(`\x1b`)。

        2. `"[2J"` :这是一个 ANSI 转义序列 ,用来清除屏幕。它告诉终端清除屏幕上的所有内容。

        所以 ,这行代码组合在一起的作用是发送一个 ANSI 转义序列给终端 ,要求它清除屏幕上的所有内容。这个功能在命令行界面中非常有用 ,可以让程序输出更清晰。

        总结一下 ,`print(chr(27) + "[2J")` 在终端中执行时会清除当前屏幕上的所有文本。
        """
        # print(chr(27) + "[2J")
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

if __name__ == '__main__':
    main()

