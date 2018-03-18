import csv
import sqlite3
from sqlite3 import Error
import sys,os,io
import lib.menotexport as menotexport

sql_command='''
        SELECT Documents.id
        FROM Documents
        LEFT JOIN DocumentFolders
            ON DocumentFolders.documentId=Documents.id
        LEFT JOIN FileHighlights
            ON DocumentFolders.documentId=FileHighlights.documentId
        LEFT JOIN Files
            ON FileHighlights.fileHash=Files.hash
        WHERE (DocumentFolders.folderId IS NULL)
        order by Documents.id
        '''

def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        print("success")
        return conn
    
    except Error as e:
        print(e)

    return None


def get_docid(conn):
    cur = conn.cursor()
    cur.execute(sql_command)
    
    rows = cur.fetchall()
    docid=[]
    for r in rows:
        docid.append(r[0])
    return docid


def main(data_base_file,abspath_filename):     

    outdir,output_filename=os.path.split(abspath_filename)

    conn = create_connection(data_base_file)

    annotations = {}

    action = ['m']

    canonical_doc_ids = get_docid(conn)

    allfolders=True

    separate= True

    verbose= True

    ret=menotexport.process(conn,outdir,annotations,canonical_doc_ids,allfolders,action,verbose)

    counter=1
    with open(abspath_filename, 'w+') as mf:
        wr= csv.writer(mf)
        for reti in ret:
            for retii in reti:
                wr.writerow(retii)
		    
