# Firebird export arguments
from about import VERSION
import argparse


def get_args(*args):
    if len(args) != 0:
        return args
    parser = argparse.ArgumentParser(description="Firebird export")

    parser.add_argument( 'path_to_db', type=str, 
                        help="Firebird server alias or database name \
                            (eg. employee) or path to database file, eg ./employee.fdb")

    parser.add_argument('--version', action='version', version='%(prog)s version ' + VERSION)
    parser.add_argument("-e", "--export", action='store_true', default=False, help="Export data")
    parser.add_argument('-b', '--brief', action='store_true', default=False,help="Shorter info")
    parser.add_argument('-l', '--limit', action='store_true', default=False,
                         help="Limit tables and fields to those in limit_sql.py")
    parser.add_argument('-m', '--maxrows', help="Max number of rows to export")

    #fixme - numsamples to be conditional on sampledata
    parser.add_argument('-s', '--sampledata', action='store_true', default=False, 
                        help="Also show sample data records")
    parser.add_argument('-n', '--numsamples', default=3, help="number of sample rows")

    parser.add_argument('-c', '--combine', action='store_true', default=False, 
                        help="Combine output into a single file")
    format = [ 'csv', 'json',] # 'excel', 'sql', 'hdf', 'pickle', 'html' ....]?
    parser.add_argument("-F", "--format", choices=format, default='csv', help="Export output format, default .CSV")
    parser.add_argument("-o", "--outdir", type=str, dest='outdir', default='Export', help="Output directory")
    parser.add_argument("-u", "--user", type=str, default='SYSDBA', help="Firebird DB username")
    parser.add_argument("-p", "--password", type=str, default='masterkey', help="Firebird DB password")


    args = parser.parse_args()
    return args
