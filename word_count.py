import csv
import sys,os
import codecs
from nltk import pos_tag
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
#from BST import BST,Node

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
    
def lemmatize_sentence(sentence,words):
    lemmatiser = WordNetLemmatizer()
    tokens = word_tokenize(sentence)
    tokens_pos = pos_tag(tokens) 
    for r in tokens_pos:
        position = get_wordnet_pos(r[1])
        if position is not None:
            words.append(lemmatiser.lemmatize(r[0], position))
        #else:
            #words.append("#None#")

def count_unigram(words):
    dic={}
    for r in words:
        if r in dic:
            dic[r]=dic[r]+1
        else:
            dic[r]=1
    return dic

def sort_by_count(dic):
    sort_list=[]
    for key, value in sorted(dic.iteritems(), key=lambda (k,v): (v,k)):
        #print "%s: %s" % (key, value)    
        sort_list.append([key,value])

    return sort_list

def main(lighlight_text_file, word_count_file):
    
    with open(lighlight_text_file,'r') as csvfile:
        reader = csv.reader(csvfile)
        words=[]
        counter=1
        for row in reader:
            #print(counter,row[3])
            row[1]=unicode(row[1], "utf-8")
            counter+=1
            words.append(lemmatize_sentence(row[1],words))
        dic = count_unigram(words)
        
        lst=sort_by_count(dic)
        print(lst)
            
    with codecs.open(word_count_file, 'w+',) as mf:
        wr = csv.writer(mf)  
        for r in lst:
            if r[0] is not None:
                row =[r[0].encode("utf-8"),str(r[1]).encode("utf-8")]
                #print(row)
                wr.writerow(row) 
            
            """    
        with codecs.open(word_count_file, 'w+',) as mf:
            wr = csv.writer(mf)  
            for r in dic:
                if r is not None:
                    row =[r.encode("utf-8"),str(dic[r]).encode("utf-8")]
                    print(row)
                    wr.writerow(row)"""
  
if __name__ == '__main__':
    #lighlight_text_file->input
    #word_count_file->output
    input_file=str(sys.argv[1])
    output_file=str(sys.argv[2])
    main(input_file,output_file)
