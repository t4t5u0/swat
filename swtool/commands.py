from swtool.color import Color
from swtool import subcommands

import sys
import inspect


def append(char):
    for item in char:
        print(f'add "{item}"')

def change():
    pass

def ls():
    pass

def kill():
    pass

def check():
    pass

def start():
    pass

def end():
    pass

def add(arg):
    for item in arg:
        print(item)
    return None

def remove():
    pass

def neko():
    print('にゃーん')

def help():
    print(
f'''コマンド一覧を表示
{'─'*100}
{'name':^10}| {'explanation':^40}| {'arguments':^50}
{'─'*100}
{'append':<10}| キャラクタを追加{' '*(40-subcommands.get_east_asian_count('キャラクタを追加'))}| キャラクタ1 キャラクタ2 キャラクタ3 ...{' '*(50-subcommands.get_east_asian_count('キャラクタ1 キャラクタ2 キャラクタ3 ...'))}
{'change':<10}| 状態を変更したいキャラクタを変更{' '*(40-subcommands.get_east_asian_count('状態を変更したいキャラクタを変更'))}| キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('キャラクタ/キャラクタID'))}
{'ls':<10}| キャラクタ一覧を表示{' '*(40-subcommands.get_east_asian_count('キャラクタ一覧を表示'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'kill':<10}| キャラクタを消去{' '*(40-subcommands.get_east_asian_count('キャラクタを消去'))}| キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('キャラクタ/キャラクタID'))}
{'add':<10}| 技能・呪文などを付与{' '*(40-subcommands.get_east_asian_count('技能・呪文などを付与'))}| 技能・呪文など 効果ラウンド上書き(オプショナル){' '*(50-subcommands.get_east_asian_count('技能・呪文など 効果ラウンド上書き(オプショナル)'))}
{'remove':<10}| 技能・呪文などを消去{' '*(40-subcommands.get_east_asian_count('技能・呪文などを消去'))}| 技能・呪文など/状態ID{' '*(50-subcommands.get_east_asian_count('技能・呪文など/状態ID'))}
{'check':<10}| 技能・呪文などの一覧を表示{' '*(40-subcommands.get_east_asian_count('技能・呪文などの一覧を表示'))}| 引数なし/キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('引数なし/キャラクタ/キャラクタID'))}
{'start':<10}| 手番を開始{' '*(40-subcommands.get_east_asian_count('手番を開始'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'end':<10}| 手番を終了{' '*(40-subcommands.get_east_asian_count('手番を終了'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'neko':<10}| にゃーん{' '*(40-subcommands.get_east_asian_count('にゃーん'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'help':<10}| これ{' '*(40-subcommands.get_east_asian_count('これ'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'stop':<10}| アプリケーションを終了させる{' '*(40-subcommands.get_east_asian_count('アプリケーションを終了させる'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'─'*100}''')

def stop():
    x = input(f'[Y/n]\n{Color.GREEN}> {Color.RESET}')
    if  x == 'Y' or x == 'y':
        exit()
    else:
        return

class Commands:
    def __init__(self):
        self.name = ''
        self.exp = ''
        self.arg = ''

    def stop(self):
        name = sys._getframe().f_code.co_name
        exp = 'アプリケーションを終了させる'
        arg = '引数なし '
        x = input(f'[Y/n]\n{Color.GREEN}>{Color.RESET}')
        if  x == 'Y' or x == 'y':
            exit()
        else:
            return

    def help(self):
        self.name = sys._getframe().f_code.co_name
        self.exp = 'これ'
        self.arg = '引数なし'
        print(help.name)
        hoge = Commands()
        print(inspect.getmembers(Commands(), inspect.ismethod))
        for x in inspect.getmembers(Commands(), inspect.ismethod):
            print(eval(f'Commands.{x}.name'))

