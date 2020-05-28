import inspect
import pathlib
import re
import sqlite3
import sys
from cmd import Cmd

from swatlib.color import Color
from swatlib.subcommands import (count_east_asian_character,
                               get_east_asian_count, serch_words_index)


class Command(Cmd):

    def __init__(self, path):
        super().__init__()
        self.current_directory = path
        self.prompt = f'{Color.GREEN}> {Color.RESET}'
        self.intro = (
            f'{Color.MAGENTA}Hello{Color.RESET}\n'
            f'{"─"*100}\n'
            f'- コマンド一覧は helps で見ることができます\n'
            f'- help cmd を使用すると cmd の詳細を見ることができます\n'
            f'{"─"*100}'
        )
        self.current_character = ''
        self.turn = None
        self.nick_pattern = re.compile(r'(ch|en|npc|oth)([0-9]*[*]|[0-9]+)')

    def nick2chara(self, characters: list) -> list:
        conn = sqlite3.connect(
            self.current_directory/"db"/"data.db", detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        tmp = []
        for char in characters:
            if re.match(self.nick_pattern, char):
                if char[-1] == '*':
                    # char[:-1]% で検索する
                    c.execute(
                        'SELECT COUNT(name) FROM character_list WHERE nick LIKE ?', (f'{char[:-1]}%',))
                    cnt = c.fetchone()[0]
                    # 存在してるかどうか
                    if cnt:
                        c.execute(
                            'SELECT name FROM character_list WHERE nick LIKE ?', (f'{char[:-1]}%',))
                        tmp += [skill[0] for skill in (c.fetchall())]
                        # print(tmp)
                    else:
                        print(f'{char}に該当するキャラクタは存在しません')
                else:
                    # charで検索する
                    c.execute(
                        'SELECT COUNT(name) FROM character_list WHERE nick = ?', (char,))
                    cnt = c.fetchone()[0]
                    # 存在してるかどうか
                    if cnt:
                        c.execute(
                            'SELECT name FROM character_list WHERE nick = ?', (char,))
                        tmp += c.fetchone()
                    else:
                        print(f'{char}に該当するキャラクタは存在しません')
            else:
                # 普通に検索
                # なかったらメッセージ出して飛ばす
                c.execute(
                    'SELECT COUNT(name) FROM character_list WHERE name = ?', (char,))
                cnt = c.fetchone()[0]
                if cnt:
                    c.execute(
                        'SELECT name FROM character_list WHERE name = ?', (char,))
                    tmp += c.fetchone()
                else:
                    print(f'{char}というキャラクタは存在しません')
        conn.close()
        characters = list(set(tmp))
        return characters

    def do_append(self, inp):
        ('キャラクタを追加するコマンド\n'
         '> append <chracters> [-n <nickname>]\n'
         'ex: > append ギルバート ルッキオラ モーラ ... -n ch1 ch2 ch3 ...\n'
         'Option: -n キャラクタにラベルをつけるときに使用する\n'
         'ch en npc oth と 数字1つ以上の組み合わせを使用できます')

        # 前処理
        # そのうちリファクタする
        try:
            a, b = inp.split('-n')
        except:
            a = inp
            b = ''
        arg = a.split()
        nicks = b.split()
        if len(arg) < len(nicks):
            print('nickの方が長い')
            return
        else:
            nicks += ['' for _ in range(len(arg)-len(nicks))]

        if arg == []:
            print('引数にキャラクタ名を指定してください')
            return
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()

        for skill, nick in zip(arg, nicks):
            c.execute(
                'SELECT COUNT (name) FROM character_list WHERE name = ?', (skill,))
            if c.fetchone()[0]:
                print(f'<{skill}> はすでに存在しています')
                continue
            c.execute(
                'INSERT INTO character_list (name, nick) VALUES (?, ?)', (skill, nick))
            print(f'<{skill}> をキャラクタリストに追加しました')
            # 入力されたキャラクタが1つのときは、自動的にcurrent_characterに設定する
            if len(arg) == 1:
                self.current_character = arg[0]
                print(f'<{self.current_character}> を効果の対象にします')
                self.prompt = f'({self.current_character}){Color.GREEN}> {Color.RESET}'
            conn.commit()
        conn.close()

    def do_nick(self, inp):
        ('すでに存在するキャラクタにニックネームをつけ、グループ化するコマンド\n'
         '使用できるのは ch, en, npc, oth, に 0-9 を加えたもの\n'
         '> nick <characters> -n <nickname>\n'
         'ex: > nick hydra -n en1')

        arg = inp.split()
        characters = []
        nicknames = []

        if '-n' in arg:
            characters = arg[:arg.index('-n')]
            nicknames = arg[arg.index('-n')+1:]
        else:
            print('> nick <characters> -n <nickname>')
            return
        if len(arg) == 0:
            print('ex: nick swift -n ch1')
            return

        for chara, nick in zip(characters, nicknames):
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            # キャラが存在するか確認
            c.execute(
                'SELECT COUNT(name) FROM character_list WHERE name = ?', (chara,))
            exist_chara = c.fetchone()
            exist_chara = int(exist_chara[0])
            if exist_chara:
                if re.fullmatch('(ch|en|npc|oth)[0-9]+', nick):
                    c.execute(
                        'UPDATE character_list SET nick = ? WHERE name = ?', (nick, chara))
                    print(f'{chara} を {nick} として登録します')
                # 非NULLなら警告出したほうが嬉しい？
                else:
                    print('ch, en, npc, oth の末尾に数字をつけた文字列のみを使用できます')
            else:
                print('キャラクタが存在しません')
        conn.commit()
        conn.close()

    def do_change(self, inp):
        ('効果対象にするキャラクタを変更するコマンド\n'
         '> change [character] \n'
         'ex: > change ギルバート')

        char = inp.split()
        if len(char) == 0:
            print('引数が少なすぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
            return
        if len(char) >= 2:
            print('引数が多すぎます。changeは引数を１つ取ります。詳細は help change で確認してください。')
            return
        char = self.nick2chara(char)
        if len(char) == 0:
            return
        self.current_character = char[0]
        print(f'<{self.current_character}> を効果の対象にします')
        self.prompt = f'({self.current_character}){Color.GREEN}> {Color.RESET}'

    def do_ls(self, inp):
        ('キャラクタ一覧を確認するコマンド'
         '> ls')
        char = inp.split()
        if len(char) != 0:
            print('ls は引数なしです。詳しくは help ls')
        else:
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            result = c.execute('SELECT name, nick FROM character_list')
            result = c.fetchall()
            if len(result) == 0:
                return
            print(f'{"name":^15}{"nick":^10}')
            print('──────────────────────────')
            for skill in result:
                print(
                    f'{skill[0]:^{15-count_east_asian_character(skill[0])}}{skill[1] if skill[1] else "":^10}')

    def do_kill(self, inp):
        ('キャラクタ削除用のコマンド\n'
         '> kill <characters or nicknames>\n'
         'ex: kill swift ch1 \n'
         '引数は1つ以上、--all を指定した場合はすべて消す\n'
         '> kill --all'
         )
        char = inp.split()
        if len(char) == 0:
            print('引数を1つ以上とります。')
            return
        elif '--all' in char:
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('DELETE FROM character_list')
            c.execute('DELETE FROM status_list')
            self.current_character = ''
            conn.commit()
            conn.close()
            print('すべてのキャラクタを削除しました')
            self.prompt = f'{Color.GREEN}> {Color.RESET}'
        else:
            char = self.nick2chara(char)
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            for skill in char:
                c.execute(
                    'SELECT COUNT (*) FROM character_list WHERE name = ?', (skill,))
                n = c.fetchone()[0]
                if n == 1:
                    c.execute(
                        'DELETE FROM status_list WHERE chara_name = ?', (skill,))
                    c.execute(
                        'DELETE FROM character_list WHERE name = ?', (skill,))
                    print(f'<{skill}> を削除しました。')
                else:
                    print(f'<{skill}> というキャラは存在しません。')
            conn.commit()
            conn.close()
        # 消去するキャラがcurrent_characterならcurrent_chara を初期化
        if self.current_character in char:
            self.current_character = ''
            self.prompt = f'{Color.GREEN}> {Color.RESET}'

    def do_check(self, inp):
        ('ステータス確認用のコマンド\n'
         '> check [characters, nicknames, --all] \n'
         'ex: > check ギルバート')
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
        print(f'{"名前":^{15-count_east_asian_character("名前")}}|'
              f'{"スキル名":^{40-count_east_asian_character("スキル名")}}'
              f'{"残りラウンド":^{15-count_east_asian_character("残りラウンド")}}'
              f'{"効果":^{20-count_east_asian_character("効果")}}')
        print('─'*100)
        if '--all' in char:
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('SELECT name FROM character_list')
            char = [skill[0] for skill in c.fetchall()]

        char = self.nick2chara(char)
        for ch in char:
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            quely = 'SELECT skill_name, skill_effect, round FROM status_list WHERE chara_name = ?;'
            result = list(c.execute(quely, (ch,)))
            if len(result) == 0:
                print(f"{ch:^15}|"
                      f"{'':^40}"
                      f"{'':^15}"
                      #   幅寄せの値が-になるとエラーを起こすからmax(,0)を噛ませる
                      f"{'':<20}")
            else:
                for i, row in enumerate(result):
                    print(f"{ch if i == 0 else '':^{15-count_east_asian_character(ch if i == 0 else '')}}|"
                          f"{row[0]:^{max(40-count_east_asian_character(row[0]), 0)}}"
                          f"{row[2]:^{15-count_east_asian_character(str(row[2]))}}"
                          #   幅寄せの値が-になるとエラーを起こすからmax(,0)を噛ませる
                          f"{row[1]:<{max(20-count_east_asian_character(row[1]), 0)}}")
            conn.close()
            print('─'*100)

    def do_start(self, inp):
        ('手番開始時のコマンド\n'
         '安全のため現在追従中のキャラクタのみに適用してください\n'
         '> start [character]\n'
         'ex: (cc)> start #追従中のキャラクタを指定するときは引数なし\n'
         'WIP: スロウとかのフラグを作ってない')
        # デフォルトではself.current_character を渡す。

        def process(c, arg):
            result = c.execute(
                "SELECT DISTINCT chara_name, skill_name, round , use_start FROM status_list WHERE chara_name = ? AND use_start = 'True'", (arg,))
            result = list(result)
            if len(list(result)) == 0:
                print('手番開始時に行う処理はありません')
            else:
                for row in result:
                    print(f'{row[1]}の処理を行ってください')

        characters = inp.split()
        if len(characters) == 0:
            if self.current_character == '':
                print('キャラクタを選択してください。 help start')
                return
            else:
                characters = [self.current_character]
        if '--all' in characters:
            conn = sqlite3.connect(
                f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
            c = conn.cursor()
            c.execute('SELECT name FROM character_list')
            characters = [skill[0] for skill in c.fetchall()]
        else:
            # とりあえず全部キャラクタにする
            characters = self.nick2chara(characters)
        conn = sqlite3.connect(f'{self.current_directory}/db/data.db')
        c = conn.cursor()
        for chara in characters:
            process(c, chara)
            c.execute(
                'SELECT chara_name, skill_name, round FROM status_list WHERE chara_name = ?', (chara,))
            round_list = c.fetchall()
            # 指定されたキャラクタの技能のラウンドをすべて1減少
            # タプルからリストに変形
            round_list = list(map(list, round_list))
            # round_list[i][2] をデクリメントする
            for i, _ in enumerate(round_list):
                if round_list[i][2] > 0:
                    round_list[i][2] -= 1
            # (chara_name, skill_name, round) のタプルで入ってくるがクエリに合わせるために軸を入れ替える
            # (round, chara_name, skill_name) の形にしたい
            round_list = [(skill[2], skill[0], skill[1])
                          for skill in round_list]
            # start したときに、round_list の末尾の要素が全ての要素にコピーされてしまう不具合
            # 技能名を指定していないから、末尾の要素ですべて上書きする
            c.executemany(
                'UPDATE status_list SET round = ? WHERE chara_name = ? AND skill_name = ?', round_list)
            c.execute(
                'DELETE FROM status_list WHERE round = 0 AND chara_name = ?', (chara,))
            conn.commit()

    def do_end(self, inp):
        ('手番終了時の処理をするコマンド\n'
         '> end [character]')
        # 保守性を上げるため、関数内関数を用いる

        def process(c, arg):
            result = c.execute(
                "SELECT DISTINCT chara_name, skill_name, round , use_end FROM status_list WHERE chara_name = ? AND use_end = 'True'", (arg,))
            result = list(result)
            if len(list(result)) == 0:
                print('手番終了時に行う処理はありません')
            else:
                for row in result:
                    print(f'{row[1]}の処理を行ってください')
            # conn.close()

        arg = inp.split()
        conn = sqlite3.connect(f'{self.current_directory}/db/data.db')
        c = conn.cursor()
        if len(arg) == 0:
            if self.current_character == '':
                print('chenge コマンドでキャラクタを指定してください')
            else:
                process(c, self.current_character)
        elif len(arg) == 1:
            process(c, arg[0])
        else:
            print('引数が多すぎます')
            return

    def do_add(self, inp):
        ('キャラクタに技能を付与するコマンド。\n'
         'キャラクタを設定していない場合は change コマンドでキャラクタを設定してください\n'
         '> add [propaties]\n'
         'ex: > add マッスル・ベア ガゼル・フット\n'
         'Option:\n'
         '-r, --round <round>\n'
         '   抵抗短縮などで、効果ラウンドをデフォルトから別のものへ上書きするときに使用する\n'
         '   直後に上書きラウンド数を指定する\n'
         'ex: > add ヘイスト -r 1\n'
         '-t, --target <characters or nicknames>\n'
         '   対象を指定して効果を付与したいときに使用する\n'
         '   ch* で ch1, ch2, ... など結構柔軟に行ける\n'
         'ex: > add ブレス -t ch*\n'
         '-t -r  は併用可能')

        # 抵抗短縮の処理
        # 複数キャラに付与できるようにする
        # nickを参照して付与できるようにする
        # それらの複合できるようにする
        # 複数技能削除する？
        # --round を実装する
        # searchすると2個あるときにバグる。.count して個数分かってれば大丈夫
        arg = inp.split()

        r_position = None
        t_position = None
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
            if t_position < r_position:
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
            characters.append(self.current_character)
        # 技能だけの時
        else:
            skills = arg
            characters.append(self.current_character)

        # nick -> chara を関数化した
        characters = self.nick2chara(characters)

        # 外側のループをキャラクタ。
        # 内側のループを技能でやる
        for char in characters:
            for skill in skills:

                # db に追加する処理をする。同じ名前の技能があれば効果ラウンドを上書きする。
                # 抵抗短縮の場合、効果ラウンドが変動するから、1つの技能につき引数を2つ取る
                # この場合、技能名 ラウンド数 としておけば、まだ処理のしようがある。
                # 技能名に対してLIKE検索を行う
                conn = sqlite3.connect(
                    f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
                c = conn.cursor()
                # INSERT する前に技能の検索を行う
                c.execute(
                    'SELECT name FROM skill_list WHERE name LIKE ?', (f'%{skill}%',))
                # fetchall するとタプルのリストで返ってくる
                skill_names = c.fetchall()
                if len(skill_names) > 1:
                    # 検索して複数見つかった場合の処理
                    for i, skill_name in enumerate(skill_names):
                        print(i, skill_name[0])
                    else:
                        try:
                            index = int(input('追加したい技能の番号を入力してください:'))
                            skill_name = skill_names[index][0]
                        except:
                            print('有効な数字を入力してください')
                            return
                elif len(skill_names) == 1:
                    skill_name = skill_names[0][0]
                else:
                    print('技能が存在しません。')
                    return

                # 技能の効果をばらしている
                c.execute(
                    'SELECT effect FROM skill_list WHERE name = ?', (skill_name,))
                effects = c.fetchone()[0].split(';')

                # choice フラグを見る
                c.execute(
                    'SELECT choice FROM skill_list WHERE name = ?', (skill_name,))
                choice_flag = c.fetchone()
                if eval(choice_flag[0]):
                    for i, effect in enumerate(effects):
                        print(i, effect)
                    try:
                        index = int(input('追加したい効果の番号を入力してください:'))
                        effects = [effects[index]]
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
                if r_position is None:
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
                            chara_name, skill_name, skill_effect, round, use_2d6, use_1d6, use_start, use_end, count, choice
                        )
                        SELECT ?, name, ?, ?, use_2d6, use_1d6, use_start, use_end, count, choice
                        FROM skill_list
                        WHERE name = ?
                        ''', (char, effect, rounds, skill_name))
                        conn.commit()
                    print(f'{char} に {skill_name} を付与しました')

    def do_rm(self, inp):
        ('追従しているキャラの技能を削除するコマンド, 一度に複数消去可\n'
         '(cc) > rm <skills>\n'
         'Option: -t ターゲットを指定\n'
         '> rm <skills> -t <characters>')

        arg = inp.split()

        skills = arg
        characters = [self.current_character]
        # -t が存在するか
        if '-t' in arg:
            characters = arg[arg.index('-t')+1:]
            skills = arg[:arg.index('-t')]
        elif self.current_character == '':
            print('対象にするキャラクタを設定してください')
            return

        if len(characters) == 0:
            print('-t の後ろにはキャラクタを1体以上指定してください')
            return

        if len(arg) == 0:
            print('rm は引数を1つ以上取ります。 help rm')
            return

        characters = self.nick2chara(characters)
        if len(characters) == 0:
            return

        conn = sqlite3.connect(f'{self.current_directory}/db/data.db')
        c = conn.cursor()
        for chara in characters:
            for item in skills:
                # skill_list の skill_name をLIKE検索する
                # 同名で複数効果を持っているものがあるから、それに対応する(ヘイストなど)
                # 効果単位ではなく技能単位で消去したい
                c.execute('SELECT skill_name FROM status_list WHERE chara_name = ? AND skill_name LIKE ?',
                          (chara, f'%{item}%'))
                # fetchall するとタプルのリストで返ってくる
                # 技能の重複を削除
                skill = c.fetchall()
                # 見つからなかったら飛ばす
                if len(skill) == 0:
                    print(f'{item} に一致する技能は存在しませんでした')
                    continue

                # 一致した技能全部が入ってる
                skill_names = list(set([item[0] for item in skill]))

                # 複数あったらfor文回す
                if len(skill_names) == 1:
                    skill_name = skill_names[0]
                else:
                    for i, skill_name in enumerate(skill_names):
                        print(i, skill_name)
                    try:
                        index = int(input('追加したい効果の番号を入力してください:'))
                        skill_name = skill_names[index]
                    except:
                        print('有効な数字を入力してください')
                        return
                c.execute('DELETE FROM status_list WHERE chara_name = ? AND skill_name = ?',
                          (chara, skill_name))
                print(f'{skill_name}を削除しました')
                conn.commit()
        conn.close()


    def do_reset(self, inp):
        '''戦闘終了時の処理コマンド。状態を初期化する'''
        arg = inp.split()
        if len(arg) != 0:
            print('reset は引数を取りません')
            return
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
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
        print(f"{'start':<10}| 手番を開始{' '*(40-get_east_asian_count('手番を開始'))}| 引数なし{' '*(50-get_east_asian_count('引数なし/キャラクタ/キャラクタID'))}")
        print(f"{'end':<10}| 手番を終了{' '*(40-get_east_asian_count('手番を終了'))}| 引数なし{' '*(50-get_east_asian_count('引数なし/キャラクタ/キャラクタID'))}")
        print(f"{'neko':<10}| にゃーん{' '*(40-get_east_asian_count('にゃーん'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'help':<10}| コマンドの詳細を見る{' '*(40-get_east_asian_count('コマンドの詳細を見る'))}| コマンド名{' '*(50-get_east_asian_count('コマンド名'))}")
        print(f"{'helps':<10}| このコマンド{' '*(40-get_east_asian_count('このコマンド'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'exit':<10}| アプリケーションを終了させる{' '*(40-get_east_asian_count('アプリケーションを終了させる'))}| 引数なし{' '*(50-get_east_asian_count('引数なし'))}")
        print(f"{'─'*100}")

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
