import curses
import curses.ascii
from curses import wrapper
import locale
import time

class Screen():
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.width, self.height = self.stdscr.getmaxyx()
        self.pad = curses.newpad(self.width, self.height*5)
        self.stdscr.scrollok(True)
        self.stdscr.idlok(True)
        self.pad.scrollok(True)
        self.pad.idlok(True)
        self.y ,self.x = 0, 0
        self.sminrow, self.smincol = 0, 0
        self.smaxrow, self.smaxcol = map(lambda x: x-1, self.pad.getmaxyx())

        self.position = 0


    def scroll(self):
        pass
    def main(self, arg):
        time.sleep(5)
        self.pad.addstr('start')
        for i in range(15):
            self.pad.addstr(i+1, 0, f'{i}')
            self.pad.refresh(self.position, 0, 0, 0, 20, 75)
            time.sleep(0.3)
        for _ in range(10):
            self.position += 1
            self.pad.refresh(self.position, 0, 0, 0, 20, 75)
            time.sleep(0.3)
            continue
        for _ in range(10):
            self.position -= 1
            self.pad.refresh(self.position, 0, 0, 0, 20, 75)
            time.sleep(0.3)
            continue
        #self.pad.refresh(self.y, self.x, self.sminrow, self.smincol, self.smaxrow, self.smaxcol)
        #self.pad.refresh(self.position, 0, 0, 0, 20, 75)
        #self.y += 1




if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    screen = Screen()
    wrapper(screen.main)
