import sqlite3


conn = sqlite3.connect('../db/character_list.db', detect_types=sqlite3.PARSE_DECLTYPES)
#conn = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
c.execute(
    '''CREATE TABLE if not exists character_list(
        chara_name   text,
        skill_name   text,
        skill_effect text,
        round        integer
        );
    ''')
conn.commit()
"""
c.execute('INSERT INTO character_list VALUES(?, ?, ?, ?);',('ギルバート', 'ガゼルフット', '敏捷＋2', 3))
c.execute('INSERT INTO character_list VALUES(?, ?, ?, ?);',('ギルバート', 'マッスルベア', '筋力＋2', 3))
c.execute('INSERT INTO character_list VALUES(?, ?, ?, ?);',('モーラ', 'プレシオン', '4以下で振り直し', 3))
conn.commit()
"""
