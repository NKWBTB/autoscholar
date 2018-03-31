import csv
import sqlite3
from sqlite3 import Error
import sys,os,io
import sqlite3
import pandas as pd
import lib.exportpdf as exportpdf
import lib.exportannotation as exportannotation
from lib.tools import printHeader, printInd, printNumHeader
from datetime import datetime
from urllib import unquote
from urlparse import urlparse
import menotexport

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

def process(db,outdir,annotations,docids,allfolders,action,separate,iszotero,verbose):

	count=0
		#------------Get raw annotation data------------
	for ii,idii in enumerate(docids):
		count+=1
		#if count==3:
		#	break
		annotations=menotexport.getHighlights(db,annotations,folderid=None,foldername=None,filterdocid=idii)

	if len(annotations)==0:
		print('\n# <Menotexport>: No annotations found among Canonical docs.')
		return exportfaillist,annofaillist,bibfaillist,risfaillist
	else:
		#---------------Reformat annotations---------------
		annotations=menotexport.reformatAnno(annotations)

			#----------Extract annotations from PDFs----------
	if len(annotations)>0:
		if verbose:
			printHeader('Extracting annotations from PDFs ...',2)
		annotations,flist=menotexport.extractAnnos(annotations,action,verbose)

		
	#------------Export annotations to txt------------
	if ('m' in action or 'n' in action) and len(annotations)>0:
		if verbose:
			printHeader('Exporting annotations to text file...',2)
		flist,ret=exportAnno(annotations,action,verbose)

		return ret

def exportAnno(annodict,action,verbose=True):

	#----------------Loop through files----------------
	annofaillist=[]

	num=len(annodict)
	docids=annodict.keys()
	ret_list=[]
	for ii,idii in enumerate(docids):

		annoii=annodict[idii]
		fii=annoii.path
		basenameii=os.path.basename(fii)
		fnameii=os.path.splitext(basenameii)[0]
		fnameii=fnameii.encode('utf8','replace')
		file_name=fnameii

		if verbose:
			printNumHeader('Exporting annos in file',ii+1,num,3)
			printInd(fnameii,4)

		#----------------------Export----------------------
		try:
			# Use default formatting
			ret=_exportAnnoFile(annoii)
			ret_list.append(ret)
		except:
			annofaillist.append(basenameii)
			continue

	return annofaillist,ret_list

#------------------Export annotations in a single PDF------------------
def _exportAnnoFile(anno,verbose=True):

	conv=lambda x:unicode(x)

	hlii=anno.highlights
	hldocid=anno.docid
	ntii=anno.notes
	path=anno.path.encode('utf8','replace')
	title=anno.meta['title'].encode('utf8','replace')
	ret_list=[]
	try:
		titleii=hlii[0].title
	except:
		titleii=ntii[0].title       
		#-----------------Write highlights-----------------
	if len(hlii)>0:
		for hljj in hlii:
			hlstr=hljj.text
			outstr=u'''{}\n'''.format(hlstr)
			outstr=outstr.encode('utf8','replace')
			ret=[hldocid,title,path,outstr]
			ret_list.append(ret)

	return ret_list


def main(data_base_file,abspath_filename):     

	outdir,output_filename=os.path.split(abspath_filename)

	conn = create_connection(data_base_file)

	annotations = {}

	action = ['m']

	canonical_doc_ids = get_docid(conn)

	allfolders=True

	separate= True

	iszotero=False

	verbose= True

	ret=process(conn,outdir,annotations,canonical_doc_ids,allfolders,action,separate,iszotero,verbose)



	counter=1
	with open(abspath_filename, 'w+') as mf:
		wr= csv.writer(mf)
		for reti in ret:
			for retii in reti:
				wr.writerow(retii)

