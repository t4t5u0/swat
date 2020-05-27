from swlib.prompt import Command
import pathlib

def main():
    path = pathlib.Path(__file__).resolve().parent
    print(path)
    Command(path).cmdloop()

if __name__ == '__main__':
    main()