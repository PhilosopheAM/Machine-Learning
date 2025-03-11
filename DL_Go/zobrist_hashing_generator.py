import random
import sys

from gotypes import Player, Point


def to_python(player_state):
    if player_state is None:
        return None

    return player_state

MAX63 = 0x7fffffffffffffff

table = {}
empty_board = 0
for row in range(1,20):
    for col in range(1,20):
        for state in (Player.black, Player.white):
            specific_code = random.randint(0, MAX63)
            table[Point(row, col), state] = specific_code

with open('zobrist_hashing_content.py', 'w') as f:
    sys.stdout = f
    print('from gotypes import Player, Point')
    print("")
    print("__all__ = ['HASH_CODE', 'EMPTY_BOARD']")
    '''
    在 Python 中,__all__ 是一个特殊的变量,它定义了一个模块的公开接口。当你使用 from module import * 语句时,只有 __all__ 列表中的名字会被导入到当前的命名空间。

    具体来说,__all__ 是一个字符串列表,其中包含了你希望从模块中导出的所有名称。这样可以控制模块的命名空间,避免不必要的名称导入。
    '''
    print('')
    print('HASH_CODE = {')
    for (point, state), hash_code in table.items():
        print('(%r, %s):%r, ' %(point,to_python(state),hash_code))
    print('}')
    print('')
    print('EMPTY_BOARD = %d' % (empty_board,))
    '''
    The string formatting symbol % in Python needs to be followed by a tuple; 
    if a single-element tuple occurs, 
    you need to make it a tuple by adding a comma (,) after the single element, 
    otherwise you will get an error "TypeError: not enough arguments for format string".
    '''
    sys.stdout = sys.__stdout__

