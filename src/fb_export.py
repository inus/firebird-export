#!/usr/bin/env python3
# Export Firebird database contents to CSV

import fdb
from shutil import rmtree
import pandas as pd
import sys
import os
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append(os.path.dirname(SCRIPT_DIR + '/fb_export'))


from args import get_args
from dftools import fix_fields
from utils import mkdirs

# Change file below to limit the tables and fields 
# exported from the employee test database
from limit_sql import SFields, STable

# check for test data
from utils import unzip_testdb
unzip_testdb()


def main(*fbe_arg):
    args = get_args(*fbe_arg)
    if os.getenv('GITHUB_ACTIONS'):
        con = fdb.connect(args.path_to_db, user=args.user, password=args.password,
                fb_library_name='/opt/firebird/lib/libfbembed.so')
    else:
        con = fdb.connect(args.path_to_db)

    print("Connected to ", con.database_name, ' via ', con.firebird_version, file=sys.stderr)

    cur = con.cursor()

    df = {}
    dbf_path, dbf_name = os.path.split(args.path_to_db)
    OUTDIR = Path(Path.cwd() / args.outdir)

    if not Path(OUTDIR).exists():
        mkdirs(Path(OUTDIR / 'Files'))

    #show all tables
    SQL = 'SELECT DISTINCT RDB$RELATION_NAME FROM RDB$RELATION_FIELDS WHERE RDB$SYSTEM_FLAG=0'
    SQLTABLES = cur.execute(SQL)
    Tables = SQLTABLES.fetchall()
    Table = [Tables[i][0].rstrip() for i in range(len(Tables))]
    Fields = {}

    if args.limit:  # Use subset in STable and SFields included from XYZ_slct.py 
        Table = STable

    print("Table = ", Table, file=sys.stderr)

    for table in Table: 
        print("Table: ", table, file=sys.stderr)

        if args.limit:
            Fields[table] = SFields[table]
        else:
            ALL_FIELDS_SQL="SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS\
                WHERE RDB$RELATION_NAME=\'" + table  + "\'"
            Field = cur.execute(ALL_FIELDS_SQL).fetchall()    
            Fields[table] = [ Field[i][0].rstrip() for i in range(len(Field)) ]

        print("Fields = ", Fields[table], file=sys.stderr)

        print("Columns = ", len(Fields[table]), file=sys.stderr)

        COUNT_SQL = "select count (*) from " + table
        Count = cur.execute(COUNT_SQL)
        print("Rows = ", Count.fetchone()[0], file=sys.stderr)

        INDEX_SQL  = "SELECT s.rdb$field_name FROM rdb$index_segments AS s \
                    LEFT JOIN rdb$relation_constraints AS rc ON (rc.rdb$index_name = s.rdb$index_name) \
                    WHERE rc.rdb$relation_name = \'" + table + "\' " + \
                    "AND rc.rdb$constraint_type = \'PRIMARY KEY\'  "

        Idx = cur.execute(INDEX_SQL)
        Index = [x[0].rstrip() for x in Idx.fetchall()]
        if not args.brief:
            print("Index", end=': ', file=sys.stderr)
            print (Index, file=sys.stderr)

        fields = ','.join(Fields[table])

        if args.maxrows :
            SQL = "SELECT FIRST " + str(args.maxrows) + ' ' + fields + " from " + table 
        else:
            SQL = "SELECT " + fields + " from " + table 

        dataQ = cur.execute(SQL)
        data = dataQ.fetchall()
        df[table] = pd.DataFrame(data, columns=Fields[table])
        df[table].reindex(index=Index) 

        fix_fields(table,df, args)

        if not args.brief:
            print("Data types: ", file=sys.stderr)
            print(df[table].dtypes, file=sys.stderr)

        if args.sampledata:
            SAMPLESQL = "SELECT FIRST " + str(args.numsamples) + ' ' + fields + " from " + table 
            data = cur.execute(SAMPLESQL)
            data = dataQ.fetchall()
            print("Sample data: " +  str(args.numsamples) + " rows", file=sys.stderr)
            for d in data: print(d, file=sys.stderr)
        
        print(file=sys.stderr)

        if args.export:

            if args.format == 'csv':
                try:
                    df_out = df[table].to_csv( header=args.nh)
                except:
                    print("Error converting DF to CSV " + table, file=sys.stderr)

            else: #JSON
                try:
                    df_out = df[table].to_json()
                except:
                    print("Error converting DF to json: " + table, file=sys.stderr)

            if args.join:
                filename = dbf_name.rstrip('.fdb') + '.' + args.format 
                fmode = 'a'
            else:
                filename = dbf_name.rstrip('.fdb') + '.' + table + '.' + args.format 
                fmode = 'w'

            if args.format == 'json': #ensure encoding
                with open(Path(OUTDIR / filename), fmode, encoding='utf-8') as fp:
                    fp.write(df_out)
            else:
                with  open( Path ( OUTDIR / filename), fmode) as fp:
                        fp.write(df_out)

    try:
        rmtree('/tmp/firebird')
    except:
        pass

if __name__ == '__main__':
    main() 

