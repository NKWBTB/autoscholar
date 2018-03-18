#---------------------Imports---------------------
import sys,os
import sqlite3
import pandas as pd
import lib.exportpdf as exportpdf
import lib.exportannotation as exportannotation
import lib.tools as tools
from tools import printHeader, printInd, printNumHeader
from datetime import datetime
from urllib import unquote
from urlparse import urlparse


#-------Fetch a column from pandas dataframe-------
fetchField=lambda x, f: x[f].unique().tolist()



class FileAnno(object):

	def __init__(self,docid,meta,highlights=None,notes=None):
		'''Obj to hold annotations (highlights+notes) in a single PDF.
		'''

		self.docid=docid
		self.meta=meta
		self.highlights=highlights
		self.notes=notes
		self.path=meta['path']
		_dir, self.filename=os.path.split(self.path)
		if _dir=='/pseudo_path':
			self.hasfile=False
		else:
			self.hasfile=True

		if highlights is None:
			self.hlpages=[]
		elif type(highlights) is dict:
			self.hlpages=highlights.keys()
			self.hlpages.sort()
		elif type(highlights) is list:
			self.hlpages=[ii.page for ii in highlights]
			self.hlpages.sort()
		else:
			raise Exception("highlights type wrong")

		if notes is None:
			self.ntpages=[]
		elif type(notes) is dict:
			self.ntpages=notes.keys()
			self.ntpages.sort()
		elif type(notes) is list:
			self.ntpages=[ii.page for ii in notes]
			self.ntpages.sort()
		else:
			raise Exception("notes type wrong")


		self.pages=list(set(self.hlpages+self.ntpages))
		self.pages.sort()


def convert2datetime(s):
	return datetime.strptime(s,'%Y-%m-%dT%H:%M:%SZ')


def converturl2abspath(url):
	'''Convert a url string to an absolute path
	This is necessary for filenames with unicode strings.
	'''

	#--------------------For linux--------------------
	path = unquote(str(urlparse(url).path)).decode("utf8") 
	path=os.path.abspath(path)

	if os.path.exists(path):
		return path
	else:
		#-------------------For windowes-------------------
		if url[5:8]==u'///':   
			url=u'file://'+url[8:]
			path=urlparse(url)
			path=os.path.join(path.netloc,path.path)
			path=unquote(str(path)).decode('utf8')
			path=os.path.abspath(path)
			return path


def getUserName(db):
	'''Query db to get user name'''

	query=\
	        '''SELECT Profiles.firstName, Profiles.lastName
    FROM Profiles
    '''
	ret=db.execute(query)
	ret=[ii for ii in ret]
	return ' '.join(ret[0])


def getMetaData(db, docid):
	'''Get meta-data of a doc by documentId.
	'''

	query=\
	        '''SELECT Documents.id,
              Documents.citationkey,
              Documents.title,
              Documents.issue,
              Documents.pages,
              Documents.publication,
              Documents.volume,
              Documents.year,
              Documents.doi,
              Documents.abstract,
              Documents.arxivId,
              Documents.chapter,
              Documents.city,
              Documents.country,
              Documents.edition,
              Documents.institution,
              Documents.isbn,
              Documents.issn,
              Documents.month,
              Documents.day,
              Documents.publisher,
              Documents.series,
              Documents.type,
              Documents.read,
              Documents.favourite,
              DocumentTags.tag,
              DocumentContributors.firstNames,
              DocumentContributors.lastName,
              DocumentKeywords.keyword
       FROM Documents
       LEFT JOIN DocumentTags
           ON DocumentTags.documentId=Documents.id
       LEFT JOIN DocumentContributors
           ON DocumentContributors.documentId=Documents.id
       LEFT JOIN DocumentKeywords
           ON DocumentKeywords.documentId=Documents.id
    '''

	#------------------Get file meta data------------------
	ret=db.execute(query)
	data=ret.fetchall()
	fields=['docid','citationkey','title','issue','pages',\
	        'publication','volume','year','doi','abstract',\
	    'arxivId','chapter','city','country','edition','institution',\
	        'isbn','issn','month','day','publisher','series','type',\
	    'read','favourite','tags','firstnames','lastname','keywords']

	df=pd.DataFrame(data=data,columns=fields)
	docdata=df[df.docid==docid]
	result={}
	for ff in fields:
		fieldii=fetchField(docdata,ff)
		result[ff]=fieldii[0] if len(fieldii)==1 else fieldii

	#-----------------Append user name-----------------
	username=getUserName(db)
	result['user_name']=username

	return result



def getHighlights(db,results=None,folderid=None,foldername=None,filterdocid=None):

	query_new =\
	        '''SELECT Files.localUrl, FileHighlightRects.page,
                    FileHighlightRects.x1, FileHighlightRects.y1,
                    FileHighlightRects.x2, FileHighlightRects.y2,
                    FileHighlights.createdTime,
                    FileHighlights.documentId,
                    DocumentFolders.folderid,
                    Folders.name,
                    FileHighlights.color
            FROM Files
            LEFT JOIN FileHighlights
                ON FileHighlights.fileHash=Files.hash
            LEFT JOIN FileHighlightRects
                ON FileHighlightRects.highlightId=FileHighlights.id
            LEFT JOIN DocumentFolders
                ON DocumentFolders.documentId=FileHighlights.documentId
            LEFT JOIN Folders
                ON Folders.id=DocumentFolders.folderid
            WHERE (FileHighlightRects.page IS NOT NULL)
    '''
	query_old =\
	        '''SELECT Files.localUrl, FileHighlightRects.page,
                    FileHighlightRects.x1, FileHighlightRects.y1,
                    FileHighlightRects.x2, FileHighlightRects.y2,
                    FileHighlights.createdTime,
                    FileHighlights.documentId,
                    DocumentFolders.folderid,
                    Folders.name
            FROM Files
            LEFT JOIN FileHighlights
                ON FileHighlights.fileHash=Files.hash
            LEFT JOIN FileHighlightRects
                ON FileHighlightRects.highlightId=FileHighlights.id
            LEFT JOIN DocumentFolders
                ON DocumentFolders.documentId=FileHighlights.documentId
            LEFT JOIN Folders
                ON Folders.id=DocumentFolders.folderid
            WHERE (FileHighlightRects.page IS NOT NULL)
    '''

	query_canonical_new =\
	        '''SELECT Files.localUrl, FileHighlightRects.page,
                    FileHighlightRects.x1, FileHighlightRects.y1,
                    FileHighlightRects.x2, FileHighlightRects.y2,
                    FileHighlights.createdTime,
                    FileHighlights.documentId,
                    FileHighlights.color
            FROM Files
            LEFT JOIN FileHighlights
                ON FileHighlights.fileHash=Files.hash
            LEFT JOIN FileHighlightRects
                ON FileHighlightRects.highlightId=FileHighlights.id
            WHERE (FileHighlightRects.page IS NOT NULL)
    '''

	query_canonical_old =\
	        '''SELECT Files.localUrl, FileHighlightRects.page,
                    FileHighlightRects.x1, FileHighlightRects.y1,
                    FileHighlightRects.x2, FileHighlightRects.y2,
                    FileHighlights.createdTime,
                    FileHighlights.documentId
            FROM Files
            LEFT JOIN FileHighlights
                ON FileHighlights.fileHash=Files.hash
            LEFT JOIN FileHighlightRects
                ON FileHighlightRects.highlightId=FileHighlights.id
            WHERE (FileHighlightRects.page IS NOT NULL)
    '''

	if folderid is not None and filterdocid is None:
		fstr='(Folders.id="%s")' %folderid
		query_new=query_new+' AND\n'+fstr
		query_old=query_old+' AND\n'+fstr

	if filterdocid is not None:
		fstr='(FileHighlights.documentId="%s")' %filterdocid
		query_new=query_canonical_new+' AND\n'+fstr
		query_old=query_canonical_old+' AND\n'+fstr

	if results is None:
		results={}

	#------------------Get highlights------------------
	try:
		ret = db.execute(query_new)
		hascolor=True
	except:
		ret = db.execute(query_old)
		hascolor=False

	for ii,r in enumerate(ret):
		pth = converturl2abspath(r[0])
		pg = r[1]
		bbox = [r[2], r[3], r[4], r[5]] 
		# [x1,y1,x2,y2], (x1,y1) being bottom-left,
		# (x2,y2) being top-right. Origin at bottom-left
		cdate = convert2datetime(r[6])
		docid=r[7]
		if filterdocid is None:
			folder=r[9]
			if hascolor:
				color=r[10]
			else:
				color=None
		else:
			folder=None
			if hascolor:
				color=r[8]
			else:
				color=None

		hlight = {'rect': bbox,\
		          'cdate': cdate,\
		  'color': color,
		          'page':pg\
		  }

		#------------Save to dict------------
		if docid in results:
			if 'highlights' in results[docid]:
				if pg in results[docid]['highlights']:
					results[docid]['highlights'][pg].append(hlight)
				else:
					results[docid]['highlights'][pg]=[hlight,]
			else:
				results[docid]['highlights']={pg:[hlight,]}
		else:
			meta=getMetaData(db, docid)
			if folder is not None:
				if meta['tags'] is None:
					tags=[folder,]
				elif type(meta['tags']) is list and folder not in meta['tags']:
					tags=meta['tags']+[folder,]
				elif type(meta['tags']) is list and folder in meta['tags']:
					tags=meta['tags']
				else:
					#tags=[meta['tags'],folder]
					# there shouldn't be anything else, should it?
					#pass
					tags=[]
			else:
				tags=meta['tags'] or []
			meta['tags']=tags
			meta['path']=pth
			meta['folder']='' if folder is None else foldername
			results[docid]={'highlights':{pg:[hlight,]}}
			results[docid]['meta']=meta

	return results


#-------------Reformat annotations to a list of FileAnnos-------------
def reformatAnno(annodict):
	'''Reformat annotations to a dict of FileAnnos

	<annodict>: dict, annotation dict. See doc in getHighlights().
	Return <annos>: dict, keys: documentId; value: FileAnno objs.
	'''
	result={}
	for kk,vv in annodict.items():
		annoii=FileAnno(kk,vv['meta'],\
		                highlights=vv.get('highlights',{}),\
		        notes=vv.get('notes',{}))
		result[kk]=annoii

	return result

def extractAnnos(annotations,action,verbose):

	faillist=[]
	annotations2={}  #keys: docid, values: extracted annotations

	#-----------Loop through documents---------------
	num=len(annotations)
	docids=annotations.keys()
	
	for ii,idii in enumerate(docids):
		annoii=annotations[idii]
		fii=annoii.path
		fnameii=annoii.filename

		if verbose:
			printNumHeader('Processing file:',ii+1,num,3)
			printInd(fnameii,4)

		if 'm' in action:
			from lib import extracthl2

			try:
				#------ Check if pdftotext is available--------
				if extracthl2.checkPdftotext():
					if verbose:
						printInd('Retrieving highlights using pdftotext ...',4,prefix='# <Menotexport>:')
					hltexts=extracthl2.extractHighlights2(fii,annoii,verbose)
				else:
					if verbose:
						printInd('Retrieving highlights using pdfminer ...',4,prefix='# <Menotexport>:')
					hltexts=extracthl2.extractHighlights(fii,annoii,verbose)
			except:
				faillist.append(fnameii)
				hltexts=[]
		else:
			hltexts=[]

	
		nttexts=[]
		annoii.highlights=hltexts
		annoii.notes=nttexts
		annotations2[idii]=annoii
		
		
		#print(hltexts)
		#shortcut
		if ii==1:
			break
	return annotations2



def process(db,outdir,annotations,docids,allfolders,action,\
                      verbose):
	
	ishighlight=False
	isnote=False
	if 'm' in action or 'p' in action:
		ishighlight=True
	if 'n' in action or 'p' in action:
		isnote=True

	#------------Get raw annotation data------------
	#count=0
	for ii,idii in enumerate(docids):		
		annotations=getHighlights(db,annotations,folderid=None,foldername=None,filterdocid=idii)	
		#count+=1
		#if count==2:
			#break
	if len(annotations)==0:
		print('\n# <Menotexport>: No annotations found among Canonical docs.')
		return None
	else:
		#---------------Reformat annotations---------------
		annotations=reformatAnno(annotations)


	#----------Extract annotations from PDFs----------
	if len(annotations)>0:
		if verbose:
			printHeader('Extracting annotations from PDFs ...',2)
		annotations=extractAnnos(annotations,action,verbose)
		
	flist,ret=exportannotation.exportAnno(annotations,action,verbose)
					
	return ret
