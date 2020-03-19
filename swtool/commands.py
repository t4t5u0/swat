from swtool.color import Color
from swtool import subcommands

def append(char):
    for item in char:
        print(f'add "{item}"')

def change():
    pass

def start():
    pass

def end():
    pass

def add():
    pass

def remove():
    pass

def ls():
    pass

def kill():
    pass

def neko():
    print('にゃーん')

def help():
    print(
f'''コマンド一覧を表示
{'-'*100}
{'name':^7}| {'explanation':^34}| {'arguments':^50}
{'-'*100}
{'append':<7}| キャラクタを追加{' '*(34-subcommands.get_east_asian_count('キャラクタを追加'))}| キャラクタ1 キャラクタ2 キャラクタ3 ...{' '*(50-subcommands.get_east_asian_count('キャラクタ1 キャラクタ2 キャラクタ3 ...'))}
{'change':<7}| 状態を変更したいキャラクタを変更{' '*(34-subcommands.get_east_asian_count('状態を変更したいキャラクタを変更'))}| キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('キャラクタ/キャラクタID'))}
{'ls':<7}| キャラクタ一覧を表示{' '*(34-subcommands.get_east_asian_count('キャラクタ一覧を表示'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'kill':<7}| キャラクタを消去{' '*(34-subcommands.get_east_asian_count('キャラクタを消去'))}| キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('キャラクタ/キャラクタID'))}
{'add':<7}| 技能・呪文などを付与{' '*(34-subcommands.get_east_asian_count('技能・呪文などを付与'))}| 技能・呪文など 効果ラウンド上書き(オプショナル){' '*(50-subcommands.get_east_asian_count('技能・呪文など 効果ラウンド上書き(オプショナル)'))}
{'remove':<7}| 技能・呪文などを消去{' '*(34-subcommands.get_east_asian_count('技能・呪文などを消去'))}| 技能・呪文など/状態ID{' '*(50-subcommands.get_east_asian_count('技能・呪文など/状態ID'))}
{'check':<7}| 技能・呪文などの一覧を表示{' '*(34-subcommands.get_east_asian_count('技能・呪文などの一覧を表示'))}| 引数なし/キャラクタ/キャラクタID{' '*(50-subcommands.get_east_asian_count('引数なし/キャラクタ/キャラクタID'))}|
{'start':<7}| 手番を開始{' '*(34-subcommands.get_east_asian_count('手番を開始'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'end':<7}| 手番を終了{' '*(34-subcommands.get_east_asian_count('手番を終了'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'neko':<7}| にゃーん{' '*(34-subcommands.get_east_asian_count('にゃーん'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'help':<7}| これ{' '*(34-subcommands.get_east_asian_count('これ'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'stop':<7}| アプリケーションを終了させる{' '*(34-subcommands.get_east_asian_count('アプリケーションを終了させる'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
{'-'*100}''')

def stop():
    x = input(f'[Y/n]\n{Color.GREEN}>{Color.RESET}')
    if  x == 'Y' or x == 'y':
        exit()
    else:
        return
