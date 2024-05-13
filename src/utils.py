#utils
import sys, fdb, os, zipfile
from pathlib import Path
#from utils import unzip 

FB_EMP_DB_ZIP = 'test/employee-fdb.zip' 
FB_EMP_DB     = 'test/employee.fdb' 
DBFILESIZE = 1114112

def trim_javastr(s):
    if type(s)== fdb.fbcore.BlobReader:
        return (s.read() ).decode()
    if s is not None:
        return s.decode('utf-8','ignore')[41::]
    else:
        return ''

def trim_subj(s):
    return s.decode('utf-8','ignore')[::12]

def decode_subj(s):
    if s==None: return ''
    if type(s)==fdb.fbcore.BlobReader:
        return unzip(s)
    if s=='': return s
    return s.decode('utf-8','ignore')

def mkdirs(p):
    if not Path(p).exists():
        try:
            Path(p).mkdir(parents=True, exist_ok=True)
        except:
            print("Error creating output directory ",p , file=sys.stderr)
            exit(1)

def unzip_testdb():
    def savezip(ZF,DestZF):
        zip = zipfile.ZipFile(ZF)            
        for zipf in zip.namelist():
            data = zip.read(zipf)
            with open(DestZF, 'wb') as fp:
                fp.write(data)
    if not os.path.isfile(FB_EMP_DB):
        if os.path.isfile(FB_EMP_DB_ZIP):
            savezip(FB_EMP_DB_ZIP, FB_EMP_DB)
        else:
            print('No zipfile for example Firebird database employee.fdb found in test/ directory')
    else:
        if os.path.getsize(FB_EMP_DB) != DBFILESIZE:
            print('Altered database employee.fdb found, renamed to .bak!')
            os.rename(FB_EMP_DB, FB_EMP_DB + '.bak')
            savezip(FB_EMP_DB_ZIP, FB_EMP_DB)

def unzip(Z):
        zip = zipfile.ZipFile(Z) 
        for zipf in zip.namelist():
            data = zip.read(zipf)
        return data