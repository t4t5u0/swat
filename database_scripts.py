# データベースの初期化などを行う
# 一通り書き終わったら、sw_tool に移動

import sqlite3
import sys

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
        2d6    Bool,
        1d6    Bool,
        count  Bool,
        choice Bool,
        resist Bool
        );
        '''
    )
    conn.commit()

def delete_character_list():
    pass

def delete_skill_list():
    pass

def delete_status_list():
    pass

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
            if '--characters' in arg:
                # なんのために作ったか忘れた
                delete_characters()
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
                exit(0)
            if '--character_list' in arg:
                # キャラクタ一覧が入ってる
                create_character_list()
            if '--characters' in arg:
                # なんのために作ったか忘れた
                pass
            if '--status_list' in arg:
                # キャラクタ毎のステータスが入ってる
                pass
            if '--skill_list' in arg:
                # ステータス変動がある技能一覧や効果の一覧が入ってる
                pass

    except:
        print('help 的なやつを出力')
        exit(0)

if __name__ == '__main__':
    main()
