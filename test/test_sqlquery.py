#Run some queries on db employee.fdb
import fdb

def test_sqlquery():
      DB="./employee.fdb"
      con=fdb.connect(DB)
      cur = con.cursor()

      SQL='SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS'
      #SQL='SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS WHERE RDB$SYSTEM_FLAG=0'

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
            #Fields[table] = [ Field[i][0].rstrip() for i in range(len(Field)) ]

      #print("Fields: ", ','.join(Fields[table]), file=sys.stderr)
      #print("Field count: ", len(Fields[table]), file=sys.stderr)


      OUT=cur.execute(SQL)
      Fields=OUT.fetchall()
      assert len(Fields) == 13
      assert Fields[7][0].rstrip() == 'PAID'
      


test_sqlquery()
