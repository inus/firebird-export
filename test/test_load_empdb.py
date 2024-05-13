from pathlib import Path
import pandas as pd

JSON=Path( Path.cwd() / 'test' / 'employee.json')

def test_load_json_empdb():
    with open(JSON) as f:
        data = f.readline()
        df=pd.DataFrame.from_dict(data.split('},'))

    assert  len(df) == 67

test_load_json_empdb()