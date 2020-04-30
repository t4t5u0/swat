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
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            # 入力されたキャラクタが1つのときは、自動的にcurrent_characterに設定する
            if len(char) == 1:
                self.current_character = char[0]
                print(f'{self.current_character} を効果の対象にします')
            for item in char:
                c.execute('SELECT COUNT (name) FROM character_list WHERE name = ?', (item,))
                if c.fetchone()[0]:
                    print(f'{item}はすでに存在しています')
                    continue
                c.execute(
                    'INSERT INTO character_list (name) VALUES (?)', (item,))
                print(f'{item} をキャラクタリストに追加しました')
            conn.commit()
            conn.close()

    def do_change(self, inp):
        '''効果対象にするキャラクタを変更するコマンド\nchange [character] ex: change ギルバート'''
        char = inp.split()
        if len(char) == 0:
            print('引数が少なすぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
        elif len(char) >= 2:
            print('引数が多すぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
        else:
            self.current_character = char[0]
            print(f'{self.current_character} を効果の対象にします')

    def do_ls(self, inp):
        '''キャラクタ一覧を確認する'''
        char = inp.split()
        if len(char) != 0:
            print('ls は引数なしです。詳しくは help ls')
        else:
            conn = sqlite3.connect('./db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            for i, item in enumerate(c.execute('SELECT name FROM character_list')):
                print(i+1, item[0])

    def do_kill(self, inp):
        '''キャラクタ削除用のコマンド。 引数は1以上、--all を指定した場合はすべて消す'''
        char = inp.split()
        if len(char) == 0:
            print('引数を1つ以上とります。')
        elif '--all' in char:
            conn = sqlite3.connect('./db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('DELETE FROM character_list')
            c.execute('DELETE FROM status_list')
            self.current_character = ''
            conn.commit()
        else:
            conn = sqlite3.connect('./db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            for item in char:
                c.execute('SELECT COUNT (*) FROM character_list WHERE name = ?', (item,))
                n = c.fetchone()[0]
                #print(n)
                if n == 1:
                    c.execute('DELETE FROM status_list WHERE name = ?', (item,))
                    c.execute('DELETE FROM character_list WHERE name = ?', (item,))
                    print(f'{item} を削除しました。')
                else:
                    print(f'{item} というキャラは存在しません。')
            conn.commit()
        conn.close()
        # 消去するキャラがcurrent_characterならcurrent_chara を初期化 
        if self.current_character in char:
            self.current_character = ''


    def do_check(self, inp):
        '''ステータス確認用のコマンド\ncheck [character] ex: check ギルバート'''
        char = inp.split()
        if len(char) == 0:
            if self.current_character == '':
                print('引数が少なすぎます。check は引数を1つとります。',end='')
                print('デフォルトでは、現在追従中のキャラクタが設定されています。',end='')
                print('詳細は help check で確認してください。')
                return
            else:
                # 下の行でスライスするからリストにキャスト
                char = [self.current_character]
        elif len(char) >= 2:
            print('引数が多すぎます。check は引数を1つとります。詳細は help check で確認してください。')
        
        char = char[0]
        conn = sqlite3.connect(
            './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            #'./db/status_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        print(char)
        for row in c.execute('SELECT skill_name, skill_effect, round FROM status_list WHERE chara_name = ?;', (char,)):
            print(
                f'skill name:{row[0]:10} skill effect:{row[1]:10} round:{row[2]:10}')
        conn.close()

    def do_start(self, inp):
        '''手番開始時の処理。start [character] '''
        # デフォルトではself.current_character を渡す。
        chara_name = inp.split()
        if len(chara_name) == 0:
            if self.current_character == '':
                print('キャラクタを選択してください。 help start')
                return
            else:
                chara_name = [self.current_character]
        elif len(chara_name) > 1:
            print('引数が多すぎます。 help start')
            return
        chara_name = chara_name[0]
        conn = sqlite3.connect('./db/data.db')
        c = conn.cursor()
        # c.execute('SELECT round FROM status_list WHERE chara_name = ?', (chara_name,))
        c.execute('SELECT chara_name, skill_name, round FROM status_list WHERE chara_name = ?', (chara_name,))
        round_list = c.fetchall()
        print(round_list)
        # あるキャラクタの技能のラウンドをすべて1減少
        # タプルからリストに変形
        round_list = [[*item] for item in round_list]
        # round_list[i][2] をデクリメントする
        round_list = list(map(lambda x: x-1 if x>0 else x, round_list))
        print(round_list)
        round_and_character = [(item, self.current_character) for item in round_list]
        print(f'round_and_character:{round_and_character}')
        # (round, chara_name) のタプルにしたい
        # start したときに、round_list の末尾の要素が全ての要素にコピーされてしまう不具合
        # 技能名を指定していないから、末尾の要素ですべて上書きする
        c.executemany('UPDATE status_list SET round = ? WHERE chara_name = ?', ((item, self.current_character) for item in round_list))
        # c.executemany('UPDATE status_list SET round = ? WHERE chara_name = ?', round_and_character)
        c.execute('DELETE FROM status_list WHERE round = 0 AND chara_name = ?', (chara_name,))
        conn.commit()


    def do_end(self):
        pass

    def do_add(self, inp):
        '''キャラクタのステータスを変化を記録します。キャラクタを設定していない場合は change コマンドでキャラクタを設定してください。
        add [propaties]
        ex: add マッスル・ベア ガゼル・フット'''
        # TODO:choise フラグを見る(ウェポン・マスターなど)
        arg = inp.split()
        if len(arg) == 0:
            print('引数が少なすぎます。check は1つ以上の引数をとります。詳細は help add で確認してください。')
        else:
            if self.current_character == '':
                print('対象にするキャラクタを設定してください')
            else:
                # スキルが存在しているかを確認しなきゃいけない
                # skill_list.db を線形探索しにいく
                # タイポがあったらレーヴェンシュタイン距離を見て、2以下のものを表示したみはある
                # -> タイポがあった箇所
                # skill_list.db には 技能が【】つきで格納されているから、それを見ないようにする必要がある
                # むしろ【】をつけてあげて、部分一致を見ればいいのでは
                #   -> これは間違いで、魔法が【】、宣言特技が<<>>
                for _, item in enumerate(arg):
                    # 数字が入ってきたときはラウンドの上書きなので無視する
                    # if type(item) is int:
                    if item in [str(i) for i in range(10)]:
                        pass
                    # db に追加する処理をする。同じ名前の技能があれば効果ラウンドを上書きする。
                    # 抵抗短縮の場合、効果ラウンドが変動するから、1つの技能につき引数を2つ取る
                    # この場合、技能名 ラウンド数 としておけば、まだ処理のしようがある。
                    # 
                    else:
                        #t = arg[i+1] if arg[i+1] in [str(i) for i in range(10)] else False
                        # LIKE句を使って検索が必要
                        # IIがあるやつの処理がめんどくさい。
                        # プレイヤーは宣言特技か魔法かその他の効果なのか区別しないで使いたい
                        conn = sqlite3.connect('./db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
                        c = conn.cursor()
                        # INSERT する前に技能の検索を行う
                        c.execute('SELECT name FROM skill_list WHERE name LIKE ?',(f'%{item}%',))
                        # fetchall するとタプルのリストで返ってくる
                        skill_names = c.fetchall()
                        print(skill_names)
                        if len(skill_names) > 1:
                            # 検索して複数見つかった場合の処理
                            for i, skill_name in enumerate(skill_names):
                                #skill_name = skill_name[0]
                                print(i, skill_name[0])
                            else:
                                try:
                                    index = int(input('追加したい技能の番号を入力してください:'))
                                    skill_name = skill_names[index][0]
                                except:
                                    print('有効な数字を入力してください')
                                    break
                                print(skill_name)
                        elif len(skill_names) == 1:
                            skill_name = skill_names[0][0]
                            print(skill_name)
                        else:
                            print('技能が存在しません。')
                            break

                        # 技能の効果をばらしている
                        c.execute('SELECT effect FROM skill_list WHERE name = ?',(skill_name,))
                        effects = c.fetchone()[0].split(';')
                        print(effects)

                        # choice フラグを見る
                        c.execute('SELECT choice FROM skill_list WHERE name = ?',(skill_name,))
                        choice_flag = c.fetchone()
                        print(f'{choice_flag[0]}')
                        if eval(f'{choice_flag[0]}'):
                            for i, effect in enumerate(effects):
                                print(i, effect)
                            else:
                                try:
                                    index = int(input('追加したい効果の番号を入力してください:'))
                                    effects = [effects[index]]
                                    #print(effect)
                                except:
                                    print('有効な数字を入力してください')
                                    break

                        # 挿入部分
                        # -> ('【エンチャント・ウェポン】',), ('【スペル・エンハンス】',)
                        # ここのLIKE句消せるから消す
                        for effect in effects:
                            c.execute('''
                            INSERT INTO status_list (
                                chara_name, skill_name, skill_effect, round, use_2d6, use_1d6, count, choice, ef_table
                            )
                            SELECT ?, name, ?, round, use_2d6, use_1d6, count, choice, ef_table
                            FROM skill_list
                            WHERE name = ?
                            ''', (self.current_character, effect, skill_name))
                            conn.commit()
                        print(f'{skill_name} to {self.current_character}')

    def do_rm(self, inp):
        '''追従しているキャラの技能を削除するコマンド, 一度に複数消去可'''
        arg = inp.split()
        if self.current_character == '':
            print('対象にするキャラクタを設定してください')
        elif len(arg) == 0:
            print('rm は引数を1つ以上取ります。 help rm')
        else:
            conn = sqlite3.connect('./db/data.db')
            c = conn.cursor()
            for item in arg:
                # skill_list の skill_name をLIKE検索する
                # 同名で複数効果を持っているものがあるから、それに対応する(ヘイストなど)
                # 効果単位ではなく技能単位で消去したい
                c.execute('SELECT skill_name FROM status_list WHERE chara_name = ? AND skill_name LIKE ?',(self.current_character, f'%{item}%'))
                # fetchall するとタプルのリストで返ってくる
                # 技能の重複を削除
                skill_names = list(set(c.fetchall()[0]))
                print(skill_names)
                for _, skill_name in enumerate(skill_names):
                    c.execute('DELETE FROM status_list WHERE chara_name = ? AND skill_name = ?',(self.current_character, skill_name))
                
                conn.commit()

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

    def do_exit(self, inp):
        '''終了用のコマンド'''        
        arg = inp.split()
        if len(arg) == 0:
            x = input('終了しますか？ [Y/n] ')
            if x == 'Y' or x == 'y':
                exit(0)
            elif x == 'N' or x == 'n':
                pass
            else:
                print('中断しました')
        else:
            print('引数が多すぎます。exit は引数を取りません。')

    def help_help(self):
        print('help cmd で cmd の説明を表示します')


if __name__ == '__main__':
    Command().cmdloop()
