import sqlite3

CREATE_TABLE = """
create table if not exists testtable (
  id      integer primary key,
  intlist IntList
);
"""

IntList = list
sqlite3.register_adapter(IntList, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter("IntList", lambda s: [int(i) for i in s.split(bytes(b';'))])

def main():
    con = sqlite3.connect(":memory:", detect_types = sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    con.execute(CREATE_TABLE)

    insert_list = [1,2,3]
    con.execute('insert into testtable values(?, ?)', (1, insert_list))
    con.commit()

    cur = con.cursor()
    cur.execute('select * from testtable;')
    assert insert_list == cur.fetchone()['intlist']

if __name__ == '__main__':
    main()