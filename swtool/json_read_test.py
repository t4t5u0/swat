import json
import pprint
import sqlite3
from collections import OrderedDict
from glob import glob

# ユーザ定義型 その1
List = list
sqlite3.register_adapter(List, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter('IntList', lambda s: [str(i) for i in s.split(bytes(b';'))])

# ユーザ定義型 その2
Bool = bool
sqlite3.register_adapter(Bool, lambda b: str(b))
sqlite3.register_converter('Bool', lambda l: bool(eval(l)))

file_list = glob('../json_data/*.json')
print(file_list)
for file_ in file_list:
    with open(file_) as f:
        df = json.load(f)

    conn = sqlite3.connect('../db/example.db', detect_types=sqlite3.PARSE_DECLTYPES)
    #conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE if not exists ex(
            name   text,
            effect List,
            type   text,
            round  integer,
            '2d6'  Bool,
            '1d6'  Bool,
            count  Bool,
            choice Bool);
        ''')

    for data in df:
        #pprint.pprint(data, width=40)
        c.execute('INSERT INTO ex VALUES(?, ?, ?, ?, ?, ?, ?, ?)',\
            (data['name'], data['effect'],data['type'], data['round'],\
            data['2d6'], data['1d6'], data['count'], data['choice']))
    conn.commit()

    #for row in c.execute('select * from ex'):
    #    print(row)

    conn.close()

conn = sqlite3.connect('../db/example.db', detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
for row in c.execute('select * from ex'):
    print(row)
