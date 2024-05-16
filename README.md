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
src/fb_export.py test/employee.fdb
```

Alternatively, the package can be built and installed, preferably in a virtual environment, to make the `fb_export` command 
available in the path.

### Run:
   View database table and field names and datatypes, from Firebird database file
  ```
  ./fb_export test/employee.fdb
```

   View database table and field names and datatypes, from database alias name,
   assumes there is a Firebird installation on the local machine with example data.

  ```
  src/fb_export.py  employee
  ```
 
 View brief information, table and field only, no data types
```
src/fb_export.py -b test/employee.fdb
```
 Export from database file to directory "Export" as CSV in separate files, one per table
```
src/fb_export.py test/employee.fdb -e -o Export
```
 Test export of only the tables and fields listed in src/limit_sql.py, to a maximum of 10 records
```
src/fb_export.py test/employee.fdb -l -m 10
```
 Test export, and also view a number (5) of sample records
from the employee database (without saving)
```
src/fb_export.py -s -n 5 test/employee.fdb
```
Create a combined JSON export file
```
src/fb_export.py test/employee.fdb  -F json -e -o test/json -c 
```

Capture the database summary info to file (bash)
```
src/fb_export.py test/employee.fdb  -b &>  tmp/fdb_info.txt
src/fb_export.py  test/employee.fdb   &>  tmp/fdb_more_info.txt
```


## Usage

```
src/fb_export.py -h
usage: fb_export.py [-h] [--version] [-e] [-b] [-l] [-m MAXROWS] [-s] [-n NUMSAMPLES] [-j] [-F {csv,json}] [-o OUTDIR] [-u USER] [-p PASSWORD] path_to_db

Firebird export

positional arguments:
  path_to_db            Firebird server alias or database name (eg. employee) or path to database file, eg ./employee.fdb

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -e, --export          Export data
  -b, --brief           Shorter info
  -l, --limit           Limit tables and fields to those in limit_sql.py
  -m MAXROWS, --maxrows MAXROWS
                        Max number of rows to export
  -s, --sampledata      Also show sample data records
  -n NUMSAMPLES, --numsamples NUMSAMPLES
                        number of sample rows
  -j, --join            Join output files
  -F {csv,json}, --format {csv,json}
                        Export output format, default .CSV
  -o OUTDIR, --outdir OUTDIR
                        Output directory
  -u USER, --user USER  Firebird DB username
  -p PASSWORD, --password PASSWORD
                        Firebird DB password



```

### Build a distribution tar.gz: 

```
  pip install build
  python -m build
```

The .whl file in the `dist` directory can then be installed with pip,
the command `fb_export` should then be available in the virtual env.

```
pip install dist/fb_export-0.2.0-py3-none-any.whl
```



## Note: Firebird 2.5 and 3+ versions

The code has been tested with a with Firebird 2.5 database file.

However, I have also verified that the same  code works with a Firebird 3
installation. FB3 and FB2.5 have incompatible on-disk file structures for the 
database files but using the fdb python library, one could load a 2.5 or 3.0 database by
pointing to the appropriate 2.5 or 3.0 fbclient.so library file. In this
way one could enable loading both the 2.5 and the 3.0 and up versions of 
Firebird databases in the same python code for comparison and/or transfer.

### Test:

To run the tests in `test/` use

  `pytest`

### Calling fb_export from python

Example:

```
# Test opening Firebase database for brief info, from python
import fb_export.fb_export as fb
fb.main("test/employee.fdb","-b")
```
To run:

`python test_fb.py`


## Using Github Actions

Firebird-export has been tested with Github Actions, 
see `.github/workflows.python-app.yml` in the repo.

To run and test the workflow on a local runner, install Docker desktop and act, 
then invoke:

`act -j build`

On failure, an SSH session will be opened to be able to debug and the key will be printed to the terminal. Either close the session when done or `touch continue` to let the workflow proceed.

[^1]: Firebird is a trademark of https://firebirdsql.org/ and is used under the 'fair use' case, https://firebirdsql.org/en/firebird-brand-faq 
