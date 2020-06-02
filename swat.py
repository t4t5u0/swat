
from swatlib.prompt import Command
import pathlib

def main():
    path = pathlib.Path(__file__).resolve().parent
    Command(path).cmdloop()

if __name__ == '__main__':
    main()