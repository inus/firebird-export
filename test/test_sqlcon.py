#Firebird-Export test opening database from file
from pathlib import Path
import fdb


def test_sqlcon():

    DB = str(Path.cwd()) +  "/test/employee.fdb" 

    con = fdb.connect(DB) #, user='SYSDBA')

    cur = con.cursor()

    SQL='SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS WHERE RDB$SYSTEM_FLAG=0'

    TABLES=cur.execute(SQL)

    Tables=TABLES.fetchall()

    Table = [ Tables[i][0].rstrip() for i in range(len(Tables)) ]

    assert Table[3] == 'EMPLOYEE'


test_sqlcon()

