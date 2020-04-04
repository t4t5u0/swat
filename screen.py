import curses
import curses.ascii
import locale
from collections import deque
from copy import deepcopy
from curses import textpad, wrapper
from itertools import count

from swtool.subcommands import get_east_asian_count

try:
    from msvcrt import getch
except ImportError:
    import sys
    import tty
    import termios
    def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)



class Screen():
    UP = -1
    DOWN = 1
    WHEEL_UP = 65536
    WHEEL_DOWN = 2097152

    def __init__(self):
        '''初期化関数'''
        #super().__init__()

        self.window = None

        self.width = 0
        self.height = 0

        self.init_curses()
        #self.items = items

        self.max_lines = curses.LINES
        self.top = 0
        #self.bottom = len(self.items)
        self.current = 0
        #self.page = self.bottom // self.max_lines

        self.cursor_x = 2
        self.cursor_y = 2

        self.raw_text = []
        self.command_history = deque()

        self.cnt_up_down = 0

    def init_curses(self):
        '''cursesを初期化する関数'''
        self.window = curses.initscr()
        self.height, self.width = self.window.getmaxyx()
        self.top, self.bottom = 0, self.height-1
        self.window.setscrreg(self.top, self.bottom)
        self.window.keypad(True)
        self.window.idlok(True)
        self.window.scrollok(True)

        curses.noecho()
        curses.cbreak()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        curses.mousemask(-1)

        self.window.addstr(0, 0, 'Hello', curses.color_pair(4))
        self.window.hline(1,0,'-', 30)
        self.window.addstr(2, 0, '>', curses.color_pair(3))
        self.window.addstr(2, 1, ' ', curses.color_pair(1))
        self.window.refresh()

    def run(self):
        '''起動用メソッド'''
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()


    def input_stream(self):
        '''入力を受け取る関数'''

        for n, _ in enumerate(count()):
            #key = getch()
            key = self.window.getch()

            # マルチバイト文字の加工
            # 日本語だと3バイトだからプールする必要がある。先頭バイトを見て
            # 残りのバイスと数が確定するからその処理を行う。
            text_pool = [key]
            if 0x00 <= key <= 0x7f:
                # 1B だから何もしなくていい
                # ascii 互換領域
                pass
            elif 0x80 <= key <= 0xbf:
                # 2文字目以降のはずだから入ってきたらおかしい
                print(key)
                exit(1)
            elif 0xc0 <= key <= 0xdf:
                # 2B ウムラウト付き文字とか
                text_pool.append(self.window.getch())
                # text_pool => [0dAAA, 0dBBB]
                # 110a aabb 10bb bbbb <= これが text_poolの中身(10進にしたもの)
                # 0b00000aaa bbbbbbbb を取り出してchar c = (char) (data[i] & 0xff);
                # 10進数にしてkeyに代入
                a, b = text_pool
                tmp = map(lambda x: bin(x)[2:], [0b00011111 & a, 0b00111111 & b])
                tmp = ''.join(item.zfill(6) for item in tmp)
                key = int(tmp,2)
            elif 0xe0 <= key <= 0xef:
                # 3B 日本語はここ
                for _ in range(2):
                    text_pool.append(self.window.getch())
                a, b, c = text_pool
                # 0b 1110xxxx 10xxyyyy 10yyyyyy
                # 0d a        b        c
                tmp = map(lambda x: bin(x)[2:], [0b00001111 & a, 0b00111111 & b, 0b00111111 & c])
                tmp = ''.join([item.zfill(6) for item in tmp])
                key = int(tmp,2)
            elif 0xf0 <= key <= 0xff:
                # 4B 見たことないけどバグ取り
                for _ in range(3):
                    text_pool.append(self.window.getch())
                a, b, c ,d = text_pool
                # 11110xxx 10xxyyyy 10yyyyzz 10zzzzzz
                tmp = map(lambda x: bin(x)[2:], [0b00000111 & a, 0b00111111 & b, 0b00111111 & c, 0b00111111 & d])
                tmp = ''.join([item.zfill(6) for item in tmp])
                key = int(tmp,2)
            else:
                #print(f'{key:3}', end='')
                #特殊キー
                pass

            # キーの判定など
            if key == curses.KEY_MOUSE:
                wheel = curses.getmouse()[4]
                if wheel == self.WHEEL_UP:
                    #self.window.addstr(0, 20, 'wheel_up  ')
                    self.scroll(self.UP)
                elif wheel == self.WHEEL_DOWN:
                    #self.window.addstr(0, 20, 'wheel_down')
                    self.scroll(self.DOWN)
            elif key == (curses.ascii.ETX):
                break
            elif key in (curses.ascii.CR, curses.ascii.LF):
                self.linefeed()
            elif key in (curses.ascii.STX, curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                #TODO 日本語を消せるようにする
                if self.cursor_x != 2:
                    #self.window.addstr(0, 12, ''.join(self.raw_text))
                    #for _ in range(get_east_asian_count(self.raw_text[self.cursor_x])):
                    #self.display(f'{self.cursor_x}')
                    self.raw_text.pop(self.cursor_x-3)
                    #self.window.addstr(0, 12, ''.join(self.raw_text)+'     ')

                    #self.window.addstr(0, 12, f'{self.cursor_x}')
                    #TODO ここおかしい

                    self.window.delch(self.cursor_y, self.cursor_x-1)
                    self.window.refresh()
                self.cursor_x = max(2, self.cursor_x-1)
                self.window.addstr(0, 12, f'{self.cursor_x:3}')
            elif key == curses.KEY_UP:
                if len(self.command_history) != 0:
                    self.cursor_x = 2
                    self.window.move(self.cursor_y, self.cursor_x)
                    self.window.clrtoeol()
                    self.window.refresh()
                    self.raw_text = []
                    self.raw_text = deepcopy(self.command_history[self.cnt_up_down])
                    self.window.addstr(self.cursor_y, self.cursor_x, f'{"".join(self.raw_text)}')
                    self.window.refresh()
                    self.cnt_up_down = min(self.cnt_up_down + 1, len(self.command_history)-1)
                    self.cursor_x = len(self.raw_text)+1
                    self.window.addstr(0, 12, f'{self.cursor_x:3}')
                    self.window.move(self.cursor_y, self.cursor_x)
                continue
            elif key == curses.KEY_DOWN:
                #self.display('KEY_DOWN')
                if len(self.command_history) != 0:
                    self.cursor_x = 2
                    self.window.addstr(0, 12, f'{self.cursor_x:3}')
                    self.window.move(self.cursor_y, self.cursor_x)
                    self.window.clrtoeol()
                    self.window.refresh()
                    self.raw_text = []
                    self.raw_text = deepcopy(self.command_history[self.cnt_up_down])
                    self.window.addstr(self.cursor_y, self.cursor_x, f'{"".join(self.raw_text)}')
                    self.window.refresh()
                    self.cnt_up_down = max(self.cnt_up_down - 1, 0)
                if self.cnt_up_down == 0:
                    self.cursor_x = 2
                    self.window.addstr(0, 12, f'{self.cursor_x:3}')
                    self.window.move(self.cursor_y, self.cursor_x)
                    self.window.clrtoeol()
                    self.window.refresh()
            elif key == curses.KEY_RIGHT:
                self.cursor_x = min(self.cursor_x + 1, len(self.raw_text)+2)
                self.window.addstr(0, 12, f'{self.cursor_x:3}')
                self.window.refresh()
                #TODO 文字列が折り返していたら、次の段にいく。そうでなければ文字列長まで
                self.window.move(self.cursor_y, self.cursor_x)
            elif key == curses.KEY_LEFT:
                self.cursor_x = max(2, self.cursor_x-1)
                self.window.addstr(0, 12, f'{self.cursor_x:3}')
                self.window.move(self.cursor_y, self.cursor_x)
            elif key == curses.KEY_RESIZE:
                self.height, self.width = self.window.getmaxyx()
                self.window.resize(self.height, self.width)
                self.window.refresh()
            elif key == 1:
                self.cursor_y, self.cursor_x = 2, 2
                self.display('^a')
                self.window.move(self.cursor_y, self.cursor_x)
            else:
                #self.raw_text.append(chr(key))
                self.display(key)
                self.window.addstr(0, 12, f'{self.cursor_x:3}')
                self.window.move(self.cursor_y, self.cursor_x)
            #TODO INSERT を検出し、overwrite と insert の切り替えを行う


    def scroll(self, direction):
        '''マウスホイールを動かしたときにWindowをスクロールする関数'''
        # TODO 画面外にいくと消えるからそれの対策しなきゃいけない。
        # もしかしたら結構構成変えなきゃいけないかも
        # 上に行くときは最初にプリントしたやつよりは上にいっちゃだめ
        if direction == self.UP:
            if self.cursor_y > 0:
                self.window.scroll(-1)
        # 下に行くときは一番下より下にいっちゃだめ
        elif direction == self.DOWN:
            if self.height-1 < self.cursor_y:
                self.window.scroll(1)

    def linefeed(self):
        '''改行したときの処理'''
        #self.display(self.cursor_y)
        #self.display(self.height)
        #self.cursor_y += 1
        if self.cursor_y == self.height-1:
            self.height += 1
            self.window.resize(self.height, self.width)
            #self.window.setscrreg(self.top, self.height-1)
            self.window.refresh()
            self.window.scroll(1)
        else:
            self.cursor_y += 1
        #self.cursor_y += 1
        self.cursor_x = 2
        self.window.move(self.cursor_y, self.cursor_x)
        self.window.addstr(self.cursor_y, self.cursor_x, f'self.cursor_y:{self.cursor_y}, self.cursor_x:{self.cursor_x}')
        self.window.addstr(0, 12, f'{self.cursor_x:3}')
        self.window.addstr(self.cursor_y, 0, '>', curses.color_pair(3))
        self.window.addstr(self.cursor_y, 1, ' ', curses.color_pair(1))
        self.window.refresh()
        #self.window.move(self.cursor_y, self.cursor_x)

        if [item for item in self.raw_text if item != ' '] != []:
            self.command_history.appendleft(self.raw_text)
        self.raw_text = []
        self.cnt_up_down = 0

    def display(self, arg):
        '''表示用関数'''
        if type(arg) is int:
            arg = chr(arg)
        # Windowの幅と高さを更新する
        #self.height, self.width = self.window.getmaxyx()

        # 処理
        # 文末でなければ、addstr ではなく insstr する
        # 折り返しの処理の関係上、self.raw_textをこの中で扱ったほうが良さそう
        if len(self.raw_text) == self.cursor_x-2:
            self.window.addstr(self.cursor_y, self.cursor_x, f'{arg}', curses.color_pair(1))
            self.raw_text.append(arg)
        else:
            self.window.insstr(self.cursor_y, self.cursor_x, f'{arg}', curses.color_pair(1))
            self.raw_text.insert(self.cursor_x-2, arg)
        #self.cursor_x += get_east_asian_count(chr(arg))
        # カーソルの折り返し処理
        if self.cursor_x + get_east_asian_count(f'{arg}') +1 >= self.width:
            self.cursor_x = 0
            self.cursor_y += 1
        else:
            self.cursor_x += get_east_asian_count(f'{arg}')
        #self.window.addstr(self.cursor_y, self.cursor_x, f'{arg}', curses.color_pair(1))

        # 表示を更新する
        self.window.refresh()

def main(arg):
    screen = Screen()
    screen.run()

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    curses.wrapper(main)
