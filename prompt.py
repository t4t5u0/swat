'''
curses から方針を切り替えてcmd モジュールでの開発を行う
'''

import inspect
import sqlite3
import sys
from cmd import Cmd

from swtool import subcommands
from swtool.color import Color


class Command(Cmd):
    prompt = f'{Color.GREEN}> {Color.RESET}'
    intro = (
        f'{Color.MAGENTA}Hello{Color.RESET}\n'
        f'{"─"*100}\n'
        f'- コマンド一覧は helps で見ることができます\n'
        f'- help cmd を使用すると cmd の詳細を見ることができます\n'
        f'{"─"*100}'
    )


    turn = 0

    # def __init__(self):
    #     self.turn = 0

    def do_append(self, inp):
        '''append キャラクタ1 キャラクタ2 キャラクタ3 ...
        
        '''
        '''append [chractor] ex: append ギルバード セシル カイン・・・・'''
        char = inp.split()
        for item in char:
            print(f'add "{item}"')

    def do_change(self, inp):
        self.current_character = inp
        print(f'{self.current_character} を追跡しています')

    def do_ls(self, inp):
        pass

    def do_kill(self, inp):
        pass

    def do_check(self, inp):
        conn = sqlite3.connect('./db/character_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
        #conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        for row in c.execute('SELECT skill_name, skill_effect, round FROM character_list WHERE chara_name == ?;', (inp,)):
            print(row)
        conn.close()

    def do_start(self):
        pass

    def do_end(self):
        pass

    def do_add(self, arg):
        if self.current_character == '':
            print('対象にするキャラクタを設定してください')
        else:
            for item in arg:
                print(f'{item} to {self.current_character}')

    def do_remove(self):
        pass

    def do_neko(self, inp):
        '''にゃーん'''
        l = inp.split()
        if len(l) == 0:
            print('にゃーん')
        else:
            print('neko は引数なしだよ')
        # print(type(inp))
        # print(f'{inp}')
        # if inp is '':
        #     print('にゃーん')
        # else:
        #     print('neko は引数なしだよ')

    def do_helps(self, inp):
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
    {'helps':<10}| これ{' '*(40-subcommands.get_east_asian_count('これ'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
    {'exit':<10}| アプリケーションを終了させる{' '*(40-subcommands.get_east_asian_count('アプリケーションを終了させる'))}| 引数なし{' '*(50-subcommands.get_east_asian_count('引数なし'))}
    {'─'*100}''')

    def do_exit(self, arg):
        x = input('終了しますか？ [Y/n] ')
        if  x == 'Y' or x == 'y':
            exit(0)
        elif x == 'N' or x == 'n':
            pass
        else:
            print('中断しました')

    def help_help(self):
        print('help cmd で cmd の説明を表示します')

Command().cmdloop()
