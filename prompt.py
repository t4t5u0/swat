import inspect
import re
import sqlite3
import sys
from cmd import Cmd

from swtool.color import Color
from swtool.subcommands import count_east_asian_character, get_east_asian_count, serch_words_index


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

    nick_pattern = re.compile(r'(ch|en|npc|oth)([0-9]*[\*]|[0-9]+)')

    def do_append(self, inp):
        '''append [chracters] ex: append ギルバート ルッキオラ モーラ ...'''
        char = inp.split()
        if char == []:
            print('引数にキャラクタ名を指定してください')
        else:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            for item in char:
                if re.fullmatch('(ch|en|npc|oth)[0-9]*', item):
                    print(f'<{item}>は名前に使えません')
                else:
                    c.execute(
                        'SELECT COUNT (name) FROM character_list WHERE name = ?', (item,))
                    if c.fetchone()[0]:
                        print(f'<{item}> はすでに存在しています')
                        continue
                    c.execute(
                        'INSERT INTO character_list (name) VALUES (?)', (item,))
                    print(f'<{item}> をキャラクタリストに追加しました')
                    # 入力されたキャラクタが1つのときは、自動的にcurrent_characterに設定する
                    if len(char) == 1:
                        self.current_character = char[0]
                        print(f'<{self.current_character}> を効果の対象にします')
                        self.prompt = f'({self.current_character}){Color.GREEN}> {Color.RESET}'
                conn.commit()
            conn.close()

    def do_nick(self, inp):
        '''ch, en, npc, oth を作る'''
        arg = inp.split()
        if len(arg) == 0:
            print('ex: nick swift as ch1')
        # キャラが存在するか確認
        # as が含まれてて長さが3か見る
        # arg[0] -> chara_name
        # arg[1] -> as
        # arg[2] -> nick
        elif arg[1] == 'as' and len(arg) == 3:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute(
                'SELECT COUNT(name) FROM character_list WHERE name = ?', (arg[0],))
            exist_chara = c.fetchone()
            exist_chara = int(exist_chara[0])
            if exist_chara:
                if re.fullmatch('(ch|en|npc|oth)[0-9]*', arg[2]):
                    c.execute(
                        'UPDATE character_list SET nick = ? WHERE name = ?', (arg[2], arg[0]))
                # 非NULLなら警告出したほうが嬉しい？
                else:
                    print('ch, en, npc, oth の末尾に数字をつけた文字列のみを使用できます')
            else:
                print('キャラクタが存在しません')
            conn.commit()
        else:
            print('ex: nick swift as ch1')

    def do_change(self, inp):
        '''効果対象にするキャラクタを変更するコマンド\nchange [character] ex: change ギルバート'''
        char = inp.split()
        if len(char) == 0:
            print('引数が少なすぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
        elif len(char) >= 2:
            print('引数が多すぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
        else:
            self.current_character = char[0]
            print(f'<{self.current_character}> を効果の対象にします')
            self.prompt = f'({self.current_character}){Color.GREEN}> {Color.RESET}'

    def do_ls(self, inp):
        '''キャラクタ一覧を確認する'''
        char = inp.split()
        if len(char) != 0:
            print('ls は引数なしです。詳しくは help ls')
        else:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            result = c.execute('SELECT name, nick FROM character_list')
            result = c.fetchall()
            # print(result)
            if len(result) == 0:
                return
            print(f'{"name":^15}{"nick":^10}')
            print('──────────────────────────')
            for item in result:
                print(
                    f'{item[0]:^{15-count_east_asian_character(item[0])}}{item[1] if item[1] else "":^10}')

    def do_kill(self, inp):
        '''キャラクタ削除用のコマンド。 引数は1つ以上、--all を指定した場合はすべて消す'''
        char = inp.split()
        if len(char) == 0:
            print('引数を1つ以上とります。')
            return
        elif '--all' in char:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('DELETE FROM character_list')
            c.execute('DELETE FROM status_list')
            self.current_character = ''
            conn.commit()
            conn.close()
            print('すべてのキャラクタを削除しました')
            self.prompt = f'{Color.GREEN}> {Color.RESET}'
        else:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            for item in char:
                c.execute(
                    'SELECT COUNT (*) FROM character_list WHERE name = ?', (item,))
                n = c.fetchone()[0]
                # print(n)
                if n == 1:
                    c.execute(
                        'DELETE FROM status_list WHERE chara_name = ?', (item,))
                    c.execute(
                        'DELETE FROM character_list WHERE name = ?', (item,))
                    print(f'<{item}> を削除しました。')
                else:
                    print(f'<{item}> というキャラは存在しません。')
            conn.commit()
            conn.close()
        # 消去するキャラがcurrent_characterならcurrent_chara を初期化
        if self.current_character in char:
            self.current_character = ''
            self.prompt = f'{Color.GREEN}> {Color.RESET}'

    def do_check(self, inp):
        '''ステータス確認用のコマンド\ncheck [character] ex: check ギルバート'''
        char = inp.split()
        if len(char) == 0:
            if self.current_character == '':
                print('引数が少なすぎます。check は引数を1つとります。', end='')
                print('デフォルトでは、現在追従中のキャラクタが設定されています。', end='')
                print('詳細は help check で確認してください。')
                return
            else:
                # 下の行でスライスするからリストにキャスト
                char = [self.current_character]
        # 複数キャラを見たいという要望があった
        # elif len(char) >= 2:
        #     print('引数が多すぎます。check は引数を1つとります。詳細は help check で確認してください。')
        print(f'{"名前":^{15-count_east_asian_character("名前")}}|'
              f'{"スキル名":^{30-count_east_asian_character("スキル名")}}'
              f'{"残りラウンド":^{15-count_east_asian_character("残りラウンド")}}'
              f'{"効果":^{20-count_east_asian_character("効果")}}')
        print('─'*100)
        if '--all' in char:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('SELECT name FROM character_list')
            char = [item[0] for item in c.fetchall()]
        for ch in char:
            conn = sqlite3.connect(
                './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            quely = 'SELECT skill_name, skill_effect, round FROM status_list WHERE chara_name = ?;'
            for i, row in enumerate(c.execute(quely, (ch,))):
                print(f"{ch if i == 0 else '':^{15-count_east_asian_character(ch if i == 0 else '')}}|"
                      f" {row[0]:^{30-count_east_asian_character(row[0])}}"
                      f" {row[2]:^{15-count_east_asian_character(str(row[2]))}}"
                      f" {row[1]:<{20-count_east_asian_character(row[1])}}")
                # print(f'skill name:{row[0]:10} skill effect:{row[1]:30} round:{row[2]:5}')
            conn.close()
            print('─'*100)

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
        c.execute(
            'SELECT chara_name, skill_name, round FROM status_list WHERE chara_name = ?', (chara_name,))
        round_list = c.fetchall()
        # あるキャラクタの技能のラウンドをすべて1減少
        # タプルからリストに変形
        round_list = list(map(list, round_list))
        # round_list[i][2] をデクリメントする
        for i, _ in enumerate(round_list):
            if round_list[i][2] > 0:
                round_list[i][2] -= 1
        #round_and_character = [(item, self.current_character) for item in round_list]
        # print(f'round_list:{round_list}')
        # (chara_name, skill_name, round) のタプルで入ってくるがクエリに合わせるために軸を入れ替える
        # (round, chara_name, skill_name) の形にしたい
        round_list = [(item[2], item[0], item[1]) for item in round_list]
        # start したときに、round_list の末尾の要素が全ての要素にコピーされてしまう不具合
        # 技能名を指定していないから、末尾の要素ですべて上書きする
        c.executemany(
            'UPDATE status_list SET round = ? WHERE chara_name = ? AND skill_name = ?', round_list)
        # c.executemany('UPDATE status_list SET round = ? WHERE chara_name = ?', round_and_character)
        c.execute(
            'DELETE FROM status_list WHERE round = 0 AND chara_name = ?', (chara_name,))
        conn.commit()

    def do_end(self, inp):
        '''手番終了時に効果が発動するものをサジェストする'''
        # 保守性を上げるため、関数内関数を用いる
        def process(arg):
            conn = sqlite3.connect('./db/data.db')
            c = conn.cursor()
            result = c.execute(
                "SELECT DISTINCT chara_name, skill_name, round , use_end FROM status_list WHERE chara_name = ? AND use_end = 'True'", (arg,))
            result = list(result)
            if len(list(result)) == 0:
                print('手番終了時に行う処理はありません')
            else:
                for row in result:
                    print(f'{row[1]}の処理を行ってください')
            conn.close()

        arg = inp.split()
        if len(arg) == 0:
            if self.current_character == '':
                print('chenge コマンドでキャラクタを指定してください')
            else:
                process(self.current_character)
        elif len(arg) == 1:
            process(arg[0])
        else:
            print('引数が多すぎます')
            return

    def do_add(self, inp):
        '''キャラクタのステータスを変化を記録します。キャラクタを設定していない場合は change コマンドでキャラクタを設定してください。
        add [propaties]
        ex: add マッスル・ベア ガゼル・フット'''
        # TODO:抵抗短縮の処理
        # TODO:複数キャラに付与できるようにする
        # TODO:nickを参照して付与できるようにする
        # TODO:それらの複合できるようにする
        # 複数技能削除する？
        # --round を実装する
        # searchすると2個あるときにバグる。.count して個数分かってれば大丈夫
        arg = inp.split()

        r_position = 0
        t_position = 0
        if '--round' in arg or '-r' in arg:
            if (arg.count('--round') + arg.count('-r')) >= 2:
                print('パラメータが不正です。-r の数は1つでなければいけません')
                return
            else:
                r_position = serch_words_index(arg, ['--round', '-r'])[0]

        if '--target' in arg or '-t' in arg:
            if (arg.count('--target') + arg.count('-t')) >= 2:
                print('パラメータが不正です。-t の数は1つでなければいけません')
                return
            else:
                t_position = serch_words_index(arg, ['--target', '-t'])[0]

        if len(arg) == 0:
            print('引数が少なすぎます。add は1つ以上の引数をとります。詳細は help add で確認してください。')
            return
        if self.current_character == '' and not t_position:
            print('対象にするキャラクタを設定してください')
            return

        # 引数系の処理を全部上でしてしまおう
        skills = []
        characters = []
        rounds = ''
        # -r -t がともに存在する時
        if r_position and t_position:
            # -t が手前に存在するとき
            if t_position  < r_position:
                skills = arg[:t_position]
                characters = arg[t_position+1:r_position]
                rounds = arg[r_position+1][0]
            # -r が手前に存在する時
            else:
                skills = arg[:r_position]
                characters = arg[t_position+1:]
                rounds = arg[r_position+1][0]
        # -t のみが存在する時
        elif t_position:
            skills = arg[:t_position]
            characters = arg[t_position+1:]
        # -r のみが存在する時
        elif r_position:
            skills = arg[:r_position]
            rounds = arg[r_position+1][0]
        # 技能だけの時
        else:
            skills = arg
            characters.append(self.current_character)
        # print(t_position, r_position)
        # print(skills, characters, rounds)
        # return


        # ch1 とか ch* とか en2 とかで入ってきたときの処理をする
        # 全部キャラクタ名に直す
        conn = sqlite3.connect('./db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        tmp = []
        for char in characters:
            if re.match(self.nick_pattern, char):
                if char[-1] == '*':
                    # char[:-1]% で検索する
                    c.execute('SELECT COUNT(name) FROM character_list WHERE nick LIKE ?', (f'{char[:-1]}%',))
                    cnt = c.fetchone()[0]
                    # print(cnt)
                    # 存在してるかどうか
                    if cnt:
                        c.execute('SELECT name FROM character_list WHERE nick LIKE ?', (f'{char[:-1]}%',))
                        tmp += [item[0] for item in (c.fetchall())]
                        # print(tmp)
                    else:
                        print(f'{char}に該当するキャラクタは存在しません')
                else:
                    # charで検索する
                    c.execute('SELECT COUNT(name) FROM character_list WHERE nick = ?', (char,))
                    cnt = c.fetchone()[0]
                    # 存在してるかどうか
                    if cnt:
                        c.execute('SELECT name FROM character_list WHERE nick = ?', (char,))
                        tmp += c.fetchone()
                    else:
                        print(f'{char}に該当するキャラクタは存在しません')
            else:
                # 普通に検索
                # なかったらメッセージ出して飛ばす
                c.execute('SELECT COUNT(name) FROM character_list WHERE name = ?', (char,))
                cnt = c.fetchone()[0]
                if cnt:
                    c.execute('SELECT name FROM character_list WHERE name = ?', (char,))
                    tmp += c.fetchone()
                else:
                    print(f'{char}というキャラクタは存在しません')
        characters = list(set(tmp))

        # 外側のループをキャラクタ。
        # 内側のループを技能でやる
        for char in characters:
            for i, skill in enumerate(skills):

                # db に追加する処理をする。同じ名前の技能があれば効果ラウンドを上書きする。
                # 抵抗短縮の場合、効果ラウンドが変動するから、1つの技能につき引数を2つ取る
                # この場合、技能名 ラウンド数 としておけば、まだ処理のしようがある。
                # 技能名に対してLIKE検索を行う
                conn = sqlite3.connect(
                    './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
                c = conn.cursor()
                # INSERT する前に技能の検索を行う
                c.execute(
                    'SELECT name FROM skill_list WHERE name LIKE ?', (f'%{skill}%',))
                # fetchall するとタプルのリストで返ってくる
                skill_names = c.fetchall()
                # print(skill_names)
                if len(skill_names) > 1:
                    # 検索して複数見つかった場合の処理
                    for j, skill_name in enumerate(skill_names):
                        #skill_name = skill_name[0]
                        print(j, skill_name[0])
                    else:
                        try:
                            index = int(input('追加したい技能の番号を入力してください:'))
                            skill_name = skill_names[index][0]
                        except:
                            print('有効な数字を入力してください')
                            return
                        # print(skill_name)
                elif len(skill_names) == 1:
                    skill_name = skill_names[0][0]
                    # print(skill_name)
                else:
                    print('技能が存在しません。')
                    return

                # 技能の効果をばらしている
                c.execute(
                    'SELECT effect FROM skill_list WHERE name = ?', (skill_name,))
                effects = c.fetchone()[0].split(';')
                # print(effects)

                # choice フラグを見る
                c.execute(
                    'SELECT choice FROM skill_list WHERE name = ?', (skill_name,))
                choice_flag = c.fetchone()
                # print(type(choice_flag[0]))
                if eval(choice_flag[0]):
                    for j, effect in enumerate(effects):
                        print(j, effect)
                    try:
                        index = int(input('追加したい効果の番号を入力してください:'))
                        effects = [effects[index]]
                        # print(effect)
                    except:
                        print('有効な数字を入力してください')
                        return

                # 挿入部分
                # -> ('【エンチャント・ウェポン】',), ('【スペル・エンハンス】',)
                # ここのLIKE句消せるから消す(消した)
                # status_list にアクセスして、技能が存在しているかを確かめる
                # 存在していなかったら、INSERT句を実行する
                # 存在しているときは、UPDATE句を実行する
                # CASE のところをPyでかく。SQLでどうやるかわかんないので

                # 同名技能がすでに存在していたら残りラウンド数を上書きする
                # -r が与えられていたら、それをそのまま使う。
                if not rounds:
                        c.execute(
                            'SELECT round FROM skill_list WHERE name = ?', (skill_name,))
                        rounds = c.fetchone()[0]
                c.execute('SELECT COUNT(*) FROM status_list WHERE chara_name = ? AND skill_name = ?;',
                            (char, skill_name))
                cnt = c.fetchone()[0]
                if cnt >= 1:
                    c.execute('UPDATE status_list SET round = ? WHERE chara_name = ? AND skill_name = ?',
                                (rounds, char, skill_name))
                    print(f'{skill_name}はすでに存在しているため上書きしました')
                else:
                    # そうでなければ新しく挿入する
                    for effect in effects:
                        c.execute('''
                        INSERT INTO status_list (
                            chara_name, skill_name, skill_effect, round, use_2d6, use_1d6, use_end, count, choice, ef_table
                        )
                        SELECT ?, name, ?, ?, use_2d6, use_1d6, use_end, count, choice, ef_table
                        FROM skill_list
                        WHERE name = ?
                        ''', (char, effect, rounds, skill_name))
                        conn.commit()
                    print(f'{char} に {skill_name} を付与しました')

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
                c.execute('SELECT skill_name FROM status_list WHERE chara_name = ? AND skill_name LIKE ?',
                          (self.current_character, f'%{item}%'))
                # fetchall するとタプルのリストで返ってくる
                # 技能の重複を削除
                skill_names = list(set(c.fetchall()[0]))
                # print(skill_names)
                for _, skill_name in enumerate(skill_names):
                    c.execute('DELETE FROM status_list WHERE chara_name = ? AND skill_name = ?',
                              (self.current_character, skill_name))
                    print(f'{skill_name}を削除しました')
                conn.commit()

    def do_reset(self, inp):
        '''戦闘終了時の処理。状態を初期化する'''
        arg = inp.split()
        if len(arg) != 0:
            print('reset は引数を取りません')
            return
        conn = sqlite3.connect(
            './db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('DELETE FROM status_list WHERE round > 0')
        conn.commit()
        print('戦闘終了')

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
        print('コマンド一覧を表示')
        print(f"{'─'*100}")
        print(f"{'name':^10}| {'explanation':^40}| {'arguments':^50}")
        print(f"{'─'*100}")
        print(f"{'append':<10}| キャラクタを追加{' '*(40-get_east_asian_count('キャラクタを追加'))}| キャラクタ1 キャラクタ2 キャラクタ3 ...{' '*(50-get_east_asian_count('キャラクタ1 キャラクタ2 キャラクタ3 ...'))}")
        print(f"{'change':<10}| 状態を変更したいキャラクタを変更{' '*(40-get_east_asian_count('状態を変更したいキャラクタを変更'))}| キャラクタ/キャラクタID{' '*(50-get_east_asian_count('キャラクタ/キャラクタID'))}")
        print(f"{'ls':<10}| キャラクタ一覧を表示{' '*(40-get_east_asian_count('キャラクタ一覧を表示'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'kill':<10}| キャラクタを消去{' '*(40-get_east_asian_count('キャラクタを消去'))}| キャラクタ/キャラクタID{' '*(50-get_east_asian_count('キャラクタ/キャラクタID'))}")
        print(f"{'add':<10}| 技能・呪文などを付与{' '*(40-get_east_asian_count('技能・呪文などを付与'))}| 技能・呪文など 効果ラウンド上書き(オプショナル){' '*(50-get_east_asian_count('技能・呪文など 効果ラウンド上書き(オプショナル)'))}")
        print(f"{'remove':<10}| 技能・呪文などを消去{' '*(40-get_east_asian_count('技能・呪文などを消去'))}| 技能・呪文など/状態ID{' '*(50-get_east_asian_count('技能・呪文など/状態ID'))}")
        print(f"{'check':<10}| 技能・呪文などの一覧を表示{' '*(40-get_east_asian_count('技能・呪文などの一覧を表示'))}| 引数なし/キャラクタ/キャラクタID{' '*(50-get_east_asian_count('引数なし/キャラクタ/キャラクタID'))}")
        print(f"{'start':<10}| 手番を開始{' '*(40-get_east_asian_count('手番を開始'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'end':<10}| 手番を終了{' '*(40-get_east_asian_count('手番を終了'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'neko':<10}| にゃーん{' '*(40-get_east_asian_count('にゃーん'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'helps':<10}| これ{' '*(40-get_east_asian_count('これ'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'exit':<10}| アプリケーションを終了させる{' '*(40-get_east_asian_count('アプリケーションを終了させる'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'─'*100}''')")

    def do_exit(self, inp):
        '''終了用のコマンド'''
        arg = inp.split()
        if len(arg) == 0:
            x = input('終了しますか？ [Y/n] ')
            if x in ['y', 'Y']:
                sys.exit()
            elif x in ['n', 'N']:
                pass
            else:
                print('中断しました')
        else:
            print('引数が多すぎます。exit は引数を取りません。')

    def help_help(self):
        print('help cmd で cmd の説明を表示します')

    def emptyline(self):
        pass

    # alias
    do_ad = do_add
    do_ch = do_change
    do_ap = do_append
    do_ck = do_check


if __name__ == '__main__':
    Command().cmdloop()
