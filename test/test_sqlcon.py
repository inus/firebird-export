# Firebird-Export test opening database from file
from pathlib import Path
import fdb
import os

DBF = "/test/employee.fdb" 


def test_sqlcon():

    DB = str(Path.cwd()) + DBF

    if os.getenv('GITHUB_ACTIONS'):
        con = fdb.connect(DB,
            fb_library_name='/opt/firebird/lib/libfbembed.so')
    else:
        con = fdb.connect(DB)

    cur = con.cursor()

    SQL='SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS WHERE RDB$SYSTEM_FLAG=0'

    TABLES=cur.execute(SQL)

    Tables=TABLES.fetchall()

    Table = [Tables[i][0].rstrip() for i in range(len(Tables))]

    assert Table[3] == 'EMPLOYEE'


test_sqlcon()
