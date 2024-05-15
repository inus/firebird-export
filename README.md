# Firebird-export

#### Export a Firebird database to CSV, JSON or other pandas format

![Firebird](logo-firebird-black.png)

Import a Firebird[^1] database to pandas dataframes, show a summary of the database table names, field names, field data types, 
and index columns, optionally extract and save table data to
  a directory, in CSV/JSON (or potentially in any other pandas format), and also extract any other binary files from the database blobs and save. A subset of the tables and fields can be specified (in python) and the number of records returned can be limited for testing purposes. Output data can be combined or into one or saved in individual files named after the tables.

----
## Quick start
You will need a python 3 installation with virtualenv and pip and a Firebird (Interbase compatible)  `.fdb` database file (or a working Firebird server). 

```git clone https://github.com/inus/firebird-export.git
virtualenv .VENV311
. .VENV311/bin/activate
pip install -r requirements.txt
pytest
fb_export -d test/employee.fdb
```


### Run:
   View database table and field names and datatypes, from Firebird database file
  ```
  ./fb_export -d test/employee.fdb
```

   View database table and field names and datatypes, from database alias name,
   assumes there is a Firebird installation on the local machine with example data.

  ```
  ./fb_export -d employee
  ```
 
 View brief information, table and field only, no data types
```
./fb_export -d test/employee.fdb -b
```
 Export from database file to directory "Export" as CSV in separate files, one per table
```
./fb_export -d  test/employee.fdb -e -o Export
```
 Test export of only the tables and fields listed in src/limit_sql.py, to a maximum of 100 records
```
./fb_export -d test/employee.fdb -l -m 100
```
 Test export, and also view a number (5) of sample records
from the employee database (without saving)
```
./fb_export -d test/employee.fdb -s -n 5 
```
Create a combined JSON export file
```
./fb_export  -d test/employee.fdb  -F json -e -o test/json -c 
```

Capture the database summary info to file (bash)
```
./fb_export -d  test/employee.fdb  -b &>  tmp/fdb_info.txt
./fb_export -d  test/employee.fdb   &>  tmp/fdb_more_info.txt
```


## Usage

```src/fb_export.py -h  (or ./fb_export )
usage: fb_export.py [-h] [--version] [-e] [-b] [-l] [-m MAXROWS] [-s] [-n NUMSAMPLES] [-c] [-F {csv,json}] [-o OUTDIR] [-u USER] [-p PASSWORD] -d PATH_TO_DB

Firebird export

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -e, --export          Export data
  -b, --brief
  -l, --limit           Limit tables and fields to those in customselect.py
  -m MAXROWS, --maxrows MAXROWS
                        Max number of rows returned in export
  -s, --sampledata      Also show sample record
  -n NUMSAMPLES, --numsamples NUMSAMPLES
                        number of sample rows
  -c, --combine         Combine output into a single file
  -F {csv,json}, --format {csv,json}
                        Export output format
  -o OUTDIR, --outdir OUTDIR
                        Output directory
  -u USER, --user USER  Firebird DB username
  -p PASSWORD, --password PASSWORD
                        Firebird DB password
  -d PATH_TO_DB, --database PATH_TO_DB
                        Firebird server alias or database name
                         (eg. employee) or full path if a file, eg ./employee.fdb

```

### Build a distribution tar.gz: 
  pip install build
  build -m 


## Note: Firebird 2.5 and 3+ versions

This has mainly been tested with Firebird 2.5 but also tested to work with Firebird 3, which
has incompatible on-disk file structures. One could specify the library to possible enable loading 
both versions of data in the same python code.

### Test:
  pytest
  

[^1]: Firebird is a trademark of https://firebirdsql.org/ and is used under the 'fair use' case, https://firebirdsql.org/en/firebird-brand-faq 
