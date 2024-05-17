# Run some queries on db employee.fdb
import fdb
import os

DB = 'test/test123.fdb'


def test_sqlcreate():

    if os.path.isfile(DB):
        print("Connecting to existing " + DB)

        if 'GITHUB_ACTIONS' in os.environ:
            con = fdb.connect(DB, fb_library_name='/opt/firebird/lib/libfbembed.so')
        else:
            con = fdb.connect(DB, user='SYSDBA', password='masterkey',) 

        cur = con.cursor()

        con.commit()

    else:
        print("Creating new" + DB)

        if os.getenv('GITHUB_ACTIONS'): # todo fixme
            con = fdb.create_database(database=DB, user='SYSDBA',
            password='masterkey', fb_library_name='/opt/firebird/lib/libfbembed.so')
        else:
            con = fdb.create_database(database=DB, user='SYSDBA',
            password='masterkey')

        cur = con.cursor()

        cur.execute("create table languages ( name varchar(20), year_released integer)")
        con.commit()

    cur.execute("insert into languages (name, year_released) values ('C',        1972)")
    cur.execute("insert into languages (name, year_released) values ('Python',   1991)")
    con.commit()

    newLanguages = [
        ('Lisp',  1958),
        ('Dylan', 1995),
     ]
    
    cur.executemany("insert into languages (name, year_released) values (?, ?)", newLanguages)
    con.commit()
    result = cur.execute("select * from languages order by year_released").fetchall()
    print(result)
    assert result[1]==('C', 1972)

    con.drop_database()

test_sqlcreate()

