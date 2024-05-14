from pathlib import Path
import pandas as pd
import sys
import subprocess
# Test load json as generated

JSON_TESTFILE=Path( Path.cwd() / 'test' / 'employee.json')

def test_load_json_empdb():

    p = Path(Path.cwd() / JSON_TESTFILE )
    if not p.exists():
        EXPORT_CMD = Path( Path.cwd() / "fb_export")
        EXPORT_DIR  = 'test/json'
        args = "-d test/employee.fdb  -F json -c -e -o test -u SYSDBA -p masterkey"
        process = subprocess.run([EXPORT_CMD, args]), 
        if process[0].returncode != 0:
            print("Can not find or generate test JSON file to load:" , p)
            exit(1)
        else:
            print("Created test export json file ", p)

    with open(p) as f:
        data = f.readline()
        df=pd.DataFrame.from_dict(data.split('},'))

    #compare to a random probe from the DF
    assert  len(''.join(df.iloc[33])) == 415


test_load_json_empdb()