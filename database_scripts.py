# データベースの初期化などを行う

import sqlite3
import sys

def make_character_list():
    conn = sqlite3.connect(
        './db/character_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS character_list(
        id     integer primary key,
        name   text);
    ''')
    conn.commit()

def make_characters():
    conn = sqlite3.connect(
        './db/characters.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS characters(
        id     integer primary key,
        );
        '''
    )
    conn.commit()

def make_status_list():
    conn = sqlite3.connect(
        './db/status_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS status_list(
        id     integer primary key,
        );
        ''')
    conn.commit()

def make_skill_list():
    conn = sqlite3.connect(
        './db/skill_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS character_list(
        id     integer primary key,
        );
        '''
    )
    conn.commit()


def main():
    arg = sys.argv
    if len(arg) == 1:
        print('引数が少なすぎます。初期化するデータベースファイルを選んでください')
        exit(0)
    try:
        if '--character_list' in arg:
            # キャラクタ一覧が入ってる
            make_character_list()
        if '--characters' in arg:
            # なんのために作ったか忘れた
            pass
        if '--status_list' in arg:
            # キャラクタ毎のステータスが入ってる
            pass
        if '--skill_list' in arg:
            # ステータス変動がある技能一覧や効果の一覧が入ってる
            pass
        if '--all' in arg:
            # 全部更新する
            make_character_list()
            pass
    except:
        print('help 的なやつを出力')

if __name__ == '__main__':
    main()
