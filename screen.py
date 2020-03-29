# -*- coding:utf-8 -*-

import curses
import curses.ascii
from curses import wrapper
from itertools import count
import locale


class Screen():
    UP = -1
    DOWN = 1

    EOT = 3
    DEL = 8
    TAB = 9
    ESC = 27
    CR  = 10
    LF  = '\n'


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

        self.cursor_x = 1
        self.cursor_y = 2

    def init_curses(self):
        '''cursesを初期化する関数'''
        self.window = curses.initscr()
        self.window.keypad(True)

        curses.noecho()
        curses.cbreak()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

       #self.current = curses.color_pair(2)

        self.height, self.width = self.window.getmaxyx()

        self.window.addstr(0, 0, 'Hello', curses.color_pair(4))
        self.window.hline(1,0,'-', 20)
        self.window.addstr(2, 0, '> ', curses.color_pair(3))
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
            key = self.window.getch()
            self.cursor_x += 1

            #print(key,end='')
            if key == curses.KEY_UP:
                # コマンドヒストリをインクリメント
                pass
            elif key == curses.KEY_DOWN:
                # コマンドヒストリをデクリメント
                pass
            elif key == curses.KEY_RIGHT:
                # カーソルを右にずらす
                pass
            elif key == curses.KEY_LEFT:
                # カーソルを左にずらす
                pass
            elif key == curses.KEY_BACKSPACE:
                # カーソルの場所から1文字削除
                pass
            elif key == curses.KEY_ENTER or key == self.CR:
                # 改行処理
                self.linefeed()
            elif key == self.EOT:
                # C-c が押されたときの処理
                curses.nocbreak()
                self.window.keypad(False)
                curses.echo()
                exit()
            elif key == self.TAB:
                # コマンド補完
                pass
            elif key == self.DEL:
                # 一文字削除 ただし、'> 'は消さない
                # つまりカーソルの左の天井が0オリジンで2になる
                pass
            #TODO:マウスホイールの上下取る
            else:
                '''その他一般の入力'''
                self.display(key)
                #self.window.addstr(0, 0, chr(key))
                #self.window.refresh()


    def scroll(self, direction):
        '''マウスホイールを動かしたときにWindowをスクロールする関数'''
        pass

    def linefeed(self):
        '''改行したときの'> 'を出す処理'''
        self.cursor_y += 1
        self.cursor_x = 1
        self.window.addstr(self.cursor_y, 0, '> ', curses.color_pair(3))
        self.window.refresh()
        self.window.move(self.cursor_y, self.cursor_x)


    def display(self, arg):
        '''表示用関数'''
        # 表示を初期化
        #self.window.erase()

        # Windowの幅と高さを更新する
        self.height, self.width = self.window.getmaxyx()

        # 処理
        self.window.addstr(self.cursor_y, self.cursor_x, f'{chr(arg)}')

        # 表示を更新する
        self.window.refresh()

def main():
    screen = Screen()
    screen.run()

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, "ja_JP.UTF-8")
    main()
