#Run some queries on db employee.fdb
import fdb
import os

def test_sqlquery():
      DB="test/employee.fdb"
      if os.getenv('GITHUB_ACTIONS'):
            con = fdb.connect('test/employee.fdb',
                         fb_library_name='/opt/firebird/lib/libfbembed.so')
      else:
            con = fdb.connect('test/employee.fdb')
      cur = con.cursor()

      SQL='SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS'

      SQLTABLES=cur.execute(SQL)
      Tables=SQLTABLES.fetchall()
      Table = [ Tables[i][0].rstrip() for i in range(len(Tables)) ]
      Fields={}

      OUT=cur.execute(SQL)
      Fields=OUT.fetchall()

      assert len(Fields) == 53
      assert Fields[52][0].rstrip() == 'SALES'

      for table in Table: 
            SQL="SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS\
                WHERE RDB$RELATION_NAME=\'" + table  + "\'"
            Field = cur.execute(SQL).fetchall()    

      OUT=cur.execute(SQL)
      Fields=OUT.fetchall()
      assert len(Fields) == 13
      assert Fields[7][0].rstrip() == 'PAID'
      


test_sqlquery()
