#main.py

from itertools import count

from swtool.process import process
from swtool.color import Color

if __name__ == '__main__':
    #起動時の処理
    print(f'\n{Color.MAGENTA}Hello{Color.RESET}\n'+'-'*20)

    #無限ループ
    for _ in count():
        txt = list(input(f'{Color.GREEN}>{Color.RESET}').split())
        process(txt)