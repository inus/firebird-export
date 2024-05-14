import pandas as pd
from io import StringIO
import sys
from pathlib import Path

TESTDIR = 'test/json'

def test_loadjson():
    files= ["COUNTRY","CUSTOMER","DEPARTMENT","EMPLOYEE", "EMPLOYEE_PROJECT", 
            "JOB", "PROJECT", "PROJ_DEPT_BUDGET", "SALARY_HISTORY", "SALES" ]

    p = Path(Path.cwd() / TESTDIR )
    if not p.exists():
        try:
            p.mkdir(parents=True, exist_ok=True)
        except:
            print("Error creating output directory ",p , file=sys.stderr)
            exit(1)
        else:
            print("run ./fb_export here to generate ")

        df = pd.DataFrame()
        for file in files:
            fname = 'employee.' + file + '.json'

            f = Path( Path.cwd() / TESTDIR / fname )

            with open(f) as fp:
                data = fp.read()
                df = pd.read_json(StringIO(data))

        assert df.iloc[0][4] ==  668044800000


test_loadjson()

