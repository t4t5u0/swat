import curses
import curses.ascii
from curses import wrapper
import locale

class Screen:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.width, self.height = self.stdscr.getmaxyx()
        self.pad = curses.newpad(self.width, self.height)
        self.y ,self.x = 0, 0
        self.sminrow, self.smincol = 0, 0
        self.smaxrow, self.smaxcol = map(lambda x: x-1, self.pad.getmaxyx())

    def scroll(self):
        pass
    def main(self, stdscr):
        while True:
            key = self.pad.getch()
            if key == curses.ascii.ETX:
                exit()
            self.pad.addstr(chr(key))
            #self.pad.refresh(self.y, self.x, self.sminrow, self.smincol, self.smaxrow, self.smaxcol)
            self.pad.refresh(0, 0, 0, 0, 20, 75)
            self.y += 1
            self.pad.move(self.y, self.x)




if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    screen = Screen()
    wrapper(screen.main)
