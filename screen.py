import curses
import curses.ascii
import locale
from curses import wrapper
from curses import textpad
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

    #EOT = 3
    DEL = chr(8)
    TAB = chr(9)
    #ESC = 27
    #CR  = 10
    LF  = chr(13)

    EOT = chr(3)
    ESC = chr(27)
    CR = chr(10)
   # SYMBOLS = {
   # '\t': 'TAB',
   # '\r': 'CR',
   # '\n': 'LF',
   # }
    FUNCTIONS = {
    'A': 'up-arrow',
    'B': 'down-arrow',
    'C': 'left-arrow',
    'D': 'right-arrow',
    }

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

        self.input_text = ''

    def init_curses(self):
        '''cursesを初期化する関数'''
        self.window = curses.initscr()

        self.height, self.width = self.window.getmaxyx()

        self.window.setscrreg(0, self.height-1)
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

       #self.current = curses.color_pair(2)

        # self.height, self.width = self.window.getmaxyx()

        self.window.addstr(0, 0, 'こんにちは', curses.color_pair(4))
        self.window.hline(1,0,'-', 30)
        self.window.addstr(2, 0, '>', curses.color_pair(3))
        self.window.addstr(2, 1, ' ', curses.color_pair(1))
        self.window.refresh()

    def run(self):
        """起動用メソッド"""
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()


    def input_stream(self):
        '''入力を受け取る関数'''
        for n, _ in enumerate(count()):
            #key = self.window.getch()
            #key = getch()
            key = self.window.getch()
            #self.window.addstr(0, 12, f'{(key)}      ')
            # メインループ
            if key == (curses.ascii.ETX):
            #if key == chr(curses.ascii.ETX):
                exit(0)
            elif key in (curses.ascii.CR, curses.ascii.LF):
            #elif key in map(chr,(curses.ascii.CR, curses.ascii.LF)):
                self.linefeed()
            #elif key in map(chr,(curses.ascii.STX, curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL)):
            elif key in (curses.ascii.STX, curses.ascii.BS, curses.KEY_BACKSPACE, curses.ascii.DEL):
                #TODO 日本語を消せるようにする

                #pre_ch = self.window.getstr(self.cursor_y, self.cursor_x)
                '''
                if curses.ascii.isascii(pre_ch):
                    # ascii の外なら2文字分消す
                    self.window.delch(self.cursor_y, self.cursor_x)
                    self.cursor_x = max(2, self.cursor_x - 1)
                    self.window.refresh()
                '''

                #self.window.addstr(0, 30, f'pre_ch: {pre_ch}   ')
                #self.window.refresh()
                #self.cursor_x = max(2, self.cursor_x - get_east_asian_count(pre_ch))
                self.cursor_x = max(2, self.cursor_x - 1)
                self.window.delch(self.cursor_y, self.cursor_x)
                self.window.move(self.cursor_y, self.cursor_x)
                self.window.refresh()
            elif key == curses.KEY_RESIZE:
                #self.display('RESIZE')
                #map(self.display, 'RESIZE')
                self.height, self.width = self.window.getmaxyx()
                self.window.resize(self.height, self.width)
                self.window.refresh()
            else:
                self.display(key)


    def scroll(self, direction):
        '''マウスホイールを動かしたときにWindowをスクロールする関数'''
        pass

    def linefeed(self):
        '''改行したときの'> 'を出す処理'''
        self.display(self.cursor_y)
        self.display(self.height)
        if self.cursor_y >= self.height-3:
            self.height += 1
            self.window.resize(self.height, self.width)
            self.window.refresh()
            self.display(str(self.height))
            if self.window.scrollok:
                self.display('SCROLL')
                #self.window.scroll(-2)
        self.cursor_y += 1
        self.cursor_x = 2
        self.window.addstr(self.cursor_y, 0, '>', curses.color_pair(3))
        self.window.addstr(self.cursor_y, 1, ' ', curses.color_pair(1))
        self.window.refresh()
        self.window.move(self.cursor_y, self.cursor_x)
        self.input_text = ''


    def display(self, arg):
        '''表示用関数'''

        # Windowの幅と高さを更新する
        self.height, self.width = self.window.getmaxyx()

        # 処理
        self.window.addstr(self.cursor_y, self.cursor_x, f'{arg}', curses.color_pair(1))
        #self.cursor_x += get_east_asian_count(chr(arg))
        if self.cursor_x + len(f'{arg}') +1 >= self.width:
            self.cursor_x = 0
            self.cursor_y += 1
        else:
            self.cursor_x += len(f'{arg}') +1

        # 表示を更新する
        self.window.refresh()

def main(arg):
    screen = Screen()
    screen.run()

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    curses.wrapper(main)
