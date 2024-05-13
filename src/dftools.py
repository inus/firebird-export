#Custom DF column cleaning
from utils import trim_javastr, trim_subj, decode_subj 
import fdb, zipfile, re
from io import BytesIO
import pandas as pd
from pathlib import Path

PKZHDR=b'PK\x03\x04\x14\x00\x08\x00\x08\x00'
PNGHDR=b'\x89PNG\r\n'
PDFHDR=b'%PDF-1.'
HTMLHDR=b'<HTML><HEAD>'
JPGHDR=b'JFIF'

def fix_fields(f, df, args):

    if f == 'ADATTACHMENT' :

        for col in df[f].columns:

            if col=='ADFILE':

                for index, row in df[f].iterrows():

                    if type(row[col]) == fdb.fbcore.BlobReader:
                        try:
                            if not row[col].closed:
                                blob = row[col].read()
                                row[col].close()
                        except:
                            row[col] = 'BLOBREADER CLOSED'

                    if not (('blob' in locals()) or ('blob' in globals())):
                        blob = row[col]

                    if type(row[col])==str:
                         blob = bytes(row[col], 'utf-8')

                    if re.search(b'Word.Doc', blob):
                            out = re.sub(r'[^\x20-\xff]',r'', blob.decode('utf-8','ignore'))
                            row['ADFILE'] = out
                            filename =  f + '-' + str(row['ADID']) + '.doc'

                    if re.search(PKZHDR, blob):
                            zip  = zipfile.ZipFile( BytesIO(blob))
                            try:
                                for zipf in zip.namelist():
                                    blob = zip.read(zipf)
                                    row['ADFILE'] = blob
                                    filename = zipf 
                            except:
                                print("x.", col, row )

                    if re.search(PNGHDR, blob):
                        filename =  f + '-' + str(row['ADID']) + '.png'

                    if re.search(JPGHDR, blob):
                        filename =  f + '-' + str(row['ADID']) + '.jpg'
                    if re.search(PDFHDR, blob):
                        filename =  f + '-' + str(row['ADID']) + '.pdf'
                    if re.search(HTMLHDR, blob):
                        blob.decode()

                    if args.export and filename != '':
                        fpath = str((Path.cwd() / args.outdir /  'Files' )) + '/' + filename
                        with  open( fpath, 'wb') as fp:
                            fp.write(blob)
                        row[col]= 'file://' + fpath

    if f == 'ADMESSAGE' :
        df[f]['ADBODY'] = df[f]['ADBODY'].apply(trim_javastr)

    if f == 'ADCONTACT' :
        df[f]['ADEMAIL'] = df[f]['ADEMAIL'].apply(trim_javastr)
