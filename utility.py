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
from subprocess import call
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
def convert_pdf_to_text(pdf_folder_name):
		
	
	#path="/home/todd/ra/autoscholar/exported pdfs"
	path=pdf_folder_name
	
	for filename in os.listdir(path):
		if filename.endswith(".pdf"):
			file_name=os.path.join(path,filename)
			call(["pdftotext",file_name])

def remove_exported_pdfs(pdf_folder_name):
	path = pdf_folder_name
	for filename in os.listdir(path):
		if filename.endswith(".pdf"):
			file_name=os.path.join(path,filename)
			call(["rm",file_name])

def process_pdf_text(pdf_folder_name,output_pdf_text_filename):
	path = pdf_folder_name
	
	#write to output file
	counter=1
	with open(output_pdf_text_filename, 'w+') as mf:
		wr= csv.writer(mf)
		for filename in os.listdir(path):
			if filename.endswith(".txt"):
				file_name=os.path.join(path,filename)
				filename, extension = os.path.splitext(filename)
				with open(file_name) as file: 
					data = file.readlines()
					for d in data:
						row=[filename,d]
						wr.writerow(row)
			
			
def export_pdf_to_folder(db,outdir):
	
	folder_name="exported pdfs"
	
	#-----------------set up parameters-----------------
	annotations = {}

	action = ['p']

	docids = get_docid(db)

	allfolders=True

	separate= True

	iszotero=False

	verbose= True	
	
	exportfaillist=[]
	annofaillist=[]
	bibfaillist=[]
	risfaillist=[]
	
	ishighlight=False
	isnote=False	
	
	for ii,idii in enumerate(docids):
		if ishighlight:
			annotations=getHighlights(db,annotations,folderid=None,foldername=None,filterdocid=idii)
		if isnote:
			annotations=getNotes(db,annotations,folderid=None,foldername=None,filterdocid=idii)
			annotations=getDocNotes(db,annotations,folderid=None,foldername=None,filterdocid=idii)
	
	if len(annotations)==0:
		print('\n# <Menotexport>: No annotations found among Canonical docs.')
		if 'b' not in action and 'p' not in action:
			return exportfaillist,annofaillist,bibfaillist,risfaillist
	else:
			#---------------Reformat annotations---------------
			annotations=reformatAnno(annotations)
	
	#------Get other docs without annotations------
	otherdocs=menotexport.getOtherCanonicalDocs(db,docids,annotations.keys())	
	
	#--------Make subdir using folder name--------
	outdir_folder=os.path.join(outdir,folder_name)
	if not os.path.isdir(outdir_folder):
		os.makedirs(outdir_folder)	
	
	if 'p' in action:
		if len(annotations)>0:
			if verbose:
				printHeader('Exporting annotated PDFs ...',2)
			flist=exportpdf.exportAnnoPdf(annotations,\
	                                  outdir_folder,verbose)
			exportfaillist.extend(flist)

		#--------Copy other PDFs to target location--------
		if len(otherdocs)>0:
			if verbose:
				printHeader('Exporting un-annotated PDFs ...',2)
			flist=exportpdf.copyPdf(otherdocs,outdir_folder,verbose)
			exportfaillist.extend(flist)
	
	return outdir_folder
	
	
def process_highlight(db,output):
	
	
	#-----------------set up parameters-----------------
	annotations = {}

	action = ['m']

	docids = get_docid(db)

	allfolders=True

	separate= True

	iszotero=False

	verbose= True
	
	count=0
		#----------------Get raw annotation data----------------
	for ii,idii in enumerate(docids):
		#count+=1
		#if count==3:
			#break
		annotations=menotexport.getHighlights(db,annotations,folderid=None,foldername=None,filterdocid=idii)

	if len(annotations)==0:
		print('\n# <Menotexport>: No annotations found among Canonical docs.')
		return exportfaillist,annofaillist,bibfaillist,risfaillist
	else:
		#Reformat
		annotations=menotexport.reformatAnno(annotations)

			
	if len(annotations)>0:
		if verbose:
			printHeader('Extracting annotations from PDFs ...',2)
		#----------------Extract annotations----------------
		annotations,flist=menotexport.extractAnnos(annotations,action,verbose)

		
	#----------------Prepare for formated output->ret----------------
	if ('m' in action or 'n' in action) and len(annotations)>0:
		if verbose:
			printHeader('Exporting annotations to text file...',2)
		flist,ret=exportAnno(annotations,action,verbose)

	#write to output file
	counter=1
	with open(output, 'w+') as mf:
		wr= csv.writer(mf)
		for reti in ret:
			for retii in reti:
				wr.writerow(retii)	

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
			#ret=[hldocid,title,path,outstr]
			ret=[title,outstr]
			ret_list.append(ret)

	return ret_list


def main(data_base_file,output_highlight_filename,output_pdf_text_filename):     

	outdir,output_filename=os.path.split(output_highlight_filename)

	conn = create_connection(data_base_file)

	#extract highlight into file
	process_highlight(conn,output_highlight_filename)
	
	
	#export all pdf into folder
	pdf_folder_name=export_pdf_to_folder(conn,outdir)
	
	
	#convert pdf to txt file
	convert_pdf_to_text(pdf_folder_name)
	
	#remove exported pdfs
	remove_exported_pdfs(pdf_folder_name)
	
	#write text from pdfs into output file
	process_pdf_text(pdf_folder_name,output_pdf_text_filename)


