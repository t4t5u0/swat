
import pathlib
import sys

from swatlib.prompt import Command


def main():
    path = pathlib.Path(sys.argv[0]).parent
    Command(path).cmdloop()

if __name__ == '__main__':
    main()
