# データベースの初期化などを行う
# 一通り書き終わったら、sw_tool に移動

import json
import sqlite3
import sys
from glob import glob

# ユーザ定義型 その1
List = list
# (lambda l: list(l) if type(l) != list else l)]))
sqlite3.register_adapter(List, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter('IntList', lambda s: [
                           str(i) for i in s.split(bytes(b';'))])

# ユーザ定義型 その2
Bool = bool
sqlite3.register_adapter(Bool, lambda b: str(b))
sqlite3.register_converter('Bool', lambda l: bool(eval(l)))


def create_character_list():
    conn = sqlite3.connect(
        './db/character_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS character_list(
        id     integer primary key,
        name   text);
    ''')
    conn.commit()
    conn.close()


def create_status_list():
    conn = sqlite3.connect(
        './db/status_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS status_list(
        id     integer primary key,
        chara_name      text,
        skill_name      text,
        skill_effect    text,
        round           integer);
        );
        ''')
    conn.commit()
    conn.close()


def create_skill_list():
    conn = sqlite3.connect(
        './db/skill_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS skill_list(
        id     integer primary key,
        name   text,
        effect List,
        type   text,
        round  integer,
        use_2d6  Bool default 'false',
        use_1d6  Bool default 'false',
        count  Bool default 'false',
        choice Bool default 'false',
        ef_table  integer default '-1'
        );
        '''
    )
    conn.commit()

    # 初期化のためにレコードを削除する
    c.execute('DELETE FROM skill_list;')

    file_list = glob('./json_data/*.json')
    for file_ in file_list:
        with open(file_) as f:
            df = json.load(f)
        for data in df:
            #pprint.pprint(data, width=40)
            c.execute('INSERT INTO skill_list(name, effect, type, round, use_2d6, use_1d6, count, choice, ef_table) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                      (data['name'], data['effect'], data['type'], data['round'], data['2d6'], data['1d6'], data['count'], data['choice'], data['table']))
            conn.commit()
    conn.close()


def delete_character_list():
    conn = sqlite3.connect('./db/character_list.db',
                           detect_types=sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('DELETE FROM character_list;')
    conn.commit()
    conn.close()


def delete_skill_list():
    conn = sqlite3.connect('./db/skill_list.db',
                           detect_types=sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('DELETE FROM skill_list;')
    conn.commit()
    conn.close()


def delete_status_list():
    conn = sqlite3.connect('./db/status_list.db',
                           detect_types=sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute('DELETE FROM status_list;')
    conn.commit()
    conn.close()


def main():
    arg = sys.argv
    if len(arg) == 1:
        print('引数が少なすぎます。初期化するデータベースファイルを選んでください')
        exit(0)
    try:
        # 削除系
        if '-d' in arg:
            if len(arg) == 2:
                print('dbを指定させるか')
                exit(0)
            if arg in '--all':
                # 全部消す
                exit(0)
            if '--character_list' in arg:
                # キャラクタ一覧が入ってる
                delete_character_list()
            if '--status_list' in arg:
                # キャラクタ毎のステータスが入ってる
                delete_status_list()
            if '--skill_list' in arg:
                # ステータス変動がある技能一覧や効果の一覧が入ってる
                delete_skill_list()

        # ファイル生成系
        else:
            if '--all' in arg:
                # 全部更新する
                create_character_list()
                create_status_list()
                create_skill_list()
                exit(0)
            if '--character_list' in arg:
                # キャラクタ一覧が入ってる
                create_character_list()
            if '--status_list' in arg:
                # キャラクタ毎のステータスが入ってる
                create_status_list()
            if '--skill_list' in arg:
                # ステータス変動がある技能一覧や効果の一覧が入ってる
                create_skill_list()

    except:
        print('help 的なやつを出力')
        exit(0)


if __name__ == '__main__':
    main()
