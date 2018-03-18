import os
from textwrap import TextWrapper
import tools
from tools import printInd, printNumHeader
import annotation_template as atemp


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
#--------------------Export highlights and/or notes--------------------
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



