import pandas as pd
import json
from io import StringIO
import os
from pathlib import Path

def test_loadjson():
#//    files = [ "app.ADMESSAGE.json", "app.ADTICKET.json", "app.ADCONTACT.json", "app.ADATTACHMENT.json"]
    files= ["COUNTRY","CUSTOMER","DEPARTMENT","EMPLOYEE", "EMPLOYEE_PROJECT", 
            "JOB", "PROJECT", "PROJ_DEPT_BUDGET", "SALARY_HISTORY", "SALES" ]

    #file = "test/employee.json"
    #df = pd.DataFrame()
    for file in files:
        fname = 'employee.' + file + '.json'
        f = Path( Path.cwd() / 'test' / 'json' / fname )
        with open(f) as fp:
            data = fp.read()
            df = pd.read_json(StringIO(data))

    assert df.iloc[0][4] ==  668044800000

    #Test saving to CSV

    df=df.to_csv()

    SAVECSV='./test/employee.csv'

    with open(SAVECSV, 'w') as fp:
        fp.write(df)

    #print('Saved json to CSV file', './export/JSON/app_json_test_read.csv')

    assert os.path.isfile(SAVECSV) == True

    assert os.path.getsize(SAVECSV) == 3293

test_loadjson()

