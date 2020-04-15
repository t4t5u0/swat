# coding: UTF-8

import sys

from swtool import database_commands

def main():
    arg = sys.argv
    if '--help' in arg:
        print('データベースの作成や削除を行うことができます')
        print('パラメータにはデータベースの名前を指定することで、そのデータベースを初期化して作成することができます')
        print('パラメータに -d を指定した場合はレコードの削除を行うことができます')
        print('$ python database_scripts.py [--all, --character_list, --skill_list, --status_list] [-d]')
        exit(0)
    if len(arg) == 1:
        print('引数が少なすぎます。作成するデータベースファイルを選んでください')
        print('$ python database_scripts.py --help')
        exit(0)
    # 削除系
    if '-d' in arg:
        if len(arg) == 2:
            print('引数が少なすぎます。作成するデータベースファイルを選んでください')
            print('$ python database_scripts.py --help')
            exit(0)
        if arg in '--all':
            # 全部消す
            database_commands.delete_character_list()
            database_commands.delete_status_list()
            database_commands.delete_skill_list()
            exit(0)
        if '--character_list' in arg:
            # キャラクタ一覧が入ってる
            database_commands.delete_character_list()
        if '--status_list' in arg:
            # キャラクタ毎のステータスが入ってる
            database_commands.delete_status_list()
        if '--skill_list' in arg:
            # ステータス変動がある技能一覧や効果の一覧が入ってる
            database_commands.delete_skill_list()

    # ファイル生成系
    else:
        if '--all' in arg:
            # 全部更新する
            database_commands.create_character_list()
            database_commands.create_status_list()
            database_commands.create_skill_list()
            exit(0)
        if '--character_list' in arg:
            # キャラクタ一覧が入ってる
            database_commands.create_character_list()
        if '--status_list' in arg:
            # キャラクタ毎のステータスが入ってる
            database_commands.create_status_list()
        if '--skill_list' in arg:
            # ステータス変動がある技能一覧や効果の一覧が入ってる
            database_commands.create_skill_list()


if __name__ == '__main__':
    main()
