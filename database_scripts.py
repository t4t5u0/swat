import sys
import pathlib

from swatlib.database_commands import DBScript

def main():
    arg = sys.argv
    path = pathlib.Path(__file__).resolve().parent
    db_command = DBScript(path)

    if '--help' in arg:
        print('データベースの作成や削除を行うことができます')
        print('パラメータにはデータベースの名前を指定することで、そのデータベースを初期化して作成することができます')
        print('パラメータに -d を指定した場合はレコードの削除を行うことができます')
        print('$ python database_scripts.py [--all, --character_list, --skill_list, --status_list] [-d]')
        return
    if len(arg) == 1:
        print('引数が少なすぎます。作成するデータベースファイルを選んでください')
        print('$ python database_scripts.py --help')
        return
    # 削除系
    if '-d' in arg:
        if len(arg) == 2:
            print('引数が少なすぎます。作成するデータベースファイルを選んでください')
            print('$ python database_scripts.py --help')
            return
        if '--all' in arg:
            # 全部消す
            db_command.delete_character_list()
            db_command.delete_status_list()
            db_command.delete_skill_list()
            return
        if '--character_list' in arg:
            # キャラクタ一覧が入ってる
            db_command.delete_character_list()
        if '--status_list' in arg:
            # キャラクタ毎のステータスが入ってる
            db_command.delete_status_list()
        if '--skill_list' in arg:
            # ステータス変動がある技能一覧や効果の一覧が入ってる
            db_command.delete_skill_list()

    # ファイル生成系
    else:
        if '--all' in arg:
            # 全部更新する
            db_command.create_character_list()
            db_command.create_status_list()
            db_command.create_skill_list()
            return
        if '--character_list' in arg:
            # キャラクタ一覧が入ってる
            db_command.create_character_list()
        if '--status_list' in arg:
            # キャラクタ毎のステータスが入ってる
            db_command.create_status_list()
        if '--skill_list' in arg:
            # ステータス変動がある技能一覧や効果の一覧が入ってる
            db_command.create_skill_list()


if __name__ == '__main__':
    main()
