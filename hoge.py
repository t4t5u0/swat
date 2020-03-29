# inputの代わりに、1文字ずつ入力を受け取る関数を用意。
# try の中はWindows用、except 野中はLinux用
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

# Unicode制御文字のエイリアス
EOT = 3
TAB = 9
ESC = 27

# メインループ
while True:
    key = ord(getch())
    if key == EOT:
        break
    elif key == TAB:
        print('keydown TAB')
    elif key == ESC:
        key = ord(getch())
        if key == ord('['):
            key = ord(getch())
            if key == ord('A'):
                print('keydown uparrow')
                continue
            elif key == ord('B'):
                print('keydown downarrow')
                continue
            elif key == ord('C'):
                print('keydown leftarrow')
                continue
            elif key == ord('D'):
                print('keydown rightarrow')
                continue
    else:
        message = f'keydown {chr(key)}'
        print(message, key)