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

    current_character = ''
    turn = 0

    def do_append(self, inp):
        '''append [chracters] ex: append ギルバート ルッキオラ モーラ ...'''
        char = inp.split()
        if char == []:
            print('引数にキャラクタ名を指定してください')
        else:
            if len(char) == 1:
                self.current_character = char[0]
            conn = sqlite3.connect(
                './db/character_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute(
                '''CREATE TABLE IF NOT EXISTS character_list(
                id     integer primary key,
                name   text);
            ''')
            for item in char:
                c.execute(
                    'INSERT INTO character_list (name) VALUES (?)', (item,))
                print(f'append "{item}"')
            conn.commit()

    def do_change(self, inp):
        self.current_character = inp
        print(f'{self.current_character} を追跡しています')

    def do_ls(self, inp):
        pass

    def do_kill(self, inp):
        pass

    def do_check(self, inp):
        '''ステータス確認用のコマンド\ncheck [character] ex: check ギルバート'''
        char = inp.split()
        if len(char) == 0:
            print('引数が少なすぎます。check は引数を1つとります。詳細は help check で確認してください。')
        elif len(char) >= 2:
            print('引数が多すぎます。check は引数を1つとります。詳細は help check で確認してください。')
        else:
            char = char[0]
            conn = sqlite3.connect('./db/status_list.db',
                                   detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            # c.execute('''CREATE TABLE IF NOT EXISTS status_list(
            #     id              integer primary key,
            #     chara_name      text,
            #     skill_name      text,
            #     skill_effect    text,
            #     round           integer);
            # ''')
            # conn.commit()
            print(char)
            for row in c.execute('SELECT skill_name, skill_effect, round FROM　status_list WHERE chara_name == ?;', (char,)):
                print(
                    f'skill name:{row[0]:10} skill effect:{row[1]:10} round:{row[2]:10}')
            conn.close()

    def do_start(self):
        pass

    def do_end(self):
        pass

    def do_add(self, inp):
        '''キャラクタのステータスを変化を記録します。キャラクタを設定していない場合は change コマンドでキャラクタを設定してください。
        add [propaties]
        ex: add マッスル・ベア ガゼル・フット'''
        arg = inp.split('引数が少なすぎます。check は1つ以上の引数をとります。詳細は help add で確認してください。')
        if len(arg) == 0:
            print()
        else:
            if self.current_character == '':
                print('対象にするキャラクタを設定してください')
            else:
                # スキルが存在しているかを確認しなきゃいけない
                # skill_list.db を線形探索しにいく
                # タイポがあったらレーヴェンシュタイン距離を見て、2以下のものを表示したみはある
                # skill_list.db には 技能が【】つきで格納されているから、それを見ないようにする必要がある
                for item in arg:
                    # db に追加する処理をする。同じ名前の技能があれば効果ラウンドを上書きする。
                    # 抵抗短縮の場合、効果ラウンドが変動するから、1つの技能につき引数を2つ取る
                    # この場合、技能名 ラウンド数 としておけば、まだ処理のしようがある。
                    # 
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
        if x == 'Y' or x == 'y':
            exit(0)
        elif x == 'N' or x == 'n':
            pass
        else:
            print('中断しました')

    def help_help(self):
        print('help cmd で cmd の説明を表示します')


if __name__ == '__main__':
    Command().cmdloop()
