import subprocess
from itertools import count

try:
    from msvcrt import getch
except ImportError:
    def getch():
            import sys
            import tty
            import termios
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

EOT = 3
CR = 13
BS = 127
TAB = 9
SPACE = 32

txt = ''
space_cnt = 0

while True:
    key = ord(getch())
    if key == EOT:
        break
    else:
        if key == CR:
            print(txt, flush=True)
            txt = ''
            space_cnt = 0
        elif key == BS:
            txt = txt[:-1]
        else:
            if key == SPACE:
                space_cnt += 1
            txt += chr(key)
            print(txt)

        '''
        message = 'input, {0}'.format(key)
        print(message)
        message = 'input, {0}'.format(chr(key))
        print(message)
        '''
       #subprocess.run('clear',shell=True)

