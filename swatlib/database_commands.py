import json
import sqlite3
from glob import glob




class DBScript():
    def __init__(self, path):
        # ユーザ定義型 その1
        List = list
        # (lambda l: list(l) if type(l) != list else l)]))
        sqlite3.register_adapter(List, lambda l: ';'.join([str(i) for i in l]))
        sqlite3.register_converter('List', lambda s: [str(i) for i in s.split(bytes(b';'))])

        # ユーザ定義型 その2
        Bool = bool
        sqlite3.register_adapter(Bool, lambda b: str(b))
        sqlite3.register_converter('Bool', lambda l: bool(eval(l)))
        self.current_directory = path


    def create_character_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS character_list(
            id     integer primary key,
            name   text,
            nick   text default NULL
            );
            ''')
        conn.commit()
        conn.close()


    def create_status_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS status_list(
            id              integer primary key,
            chara_name      text,
            skill_name      text,
            skill_effect    text,
            type            text default "",
            round           integer,
            use_start       Bool,
            use_end         Bool,
            count           Bool,
            choice          Bool)
            ''')
        conn.commit()
        conn.close()


    def create_skill_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS skill_list(
            id     integer primary key,
            name   text,
            effect List,
            type   text,
            round  integer,
            use_start Bool default 'false',
            use_end Bool default 'false',
            count  Bool default 'false',
            choice Bool default 'false'
            );
            '''
        )
        conn.commit()

        # 初期化のためにレコードを削除する
        c.execute('DELETE FROM skill_list;')
        print('ok')
        file_list = glob(f'{self.current_directory}/json_data/*.json')
        for file_ in file_list:
            with open(file_, encoding='utf8') as f:
                df = json.load(f)
            for data in df:
                #pprint.pprint(data, width=40)
                c.execute('INSERT INTO skill_list(name, effect, type, round, use_start, use_end, count, choice) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                        (data['name'], data['effect'], data['type'], data['round'], data['start'], data['end'], data['count'], data['choice']))
                conn.commit()
        conn.close()


    def delete_character_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('DROP TABLE character_list;')
        conn.commit()
        conn.close()

    def delete_skill_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('DROP TABLE skill_list;')
        conn.commit()
        conn.close()


    def delete_status_list(self):
        conn = sqlite3.connect(
            f'{self.current_directory}/db/data.db', detect_types=sqlite3.PARSE_DECLTYPES)
        c = conn.cursor()
        c.execute('DROP TABLE status_list;')
        conn.commit()
        conn.close()