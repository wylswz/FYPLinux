import nltk
import math
import string
import argparse
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

###################arugument list here######################
#parser = argparse.ArgumentParser(description='cooccurance')

############################################################
QLength = 0
CLength = 9999

def get_tokens(dir):
    with open(dir,'r') as opener:
         text = opener.read()
         tokens = nltk.word_tokenize(text)
         return tokens

def get_idf_co(c,w,tokens):
    N = len(tokens)
    NC = 0.001
    NW = 0.001
    co = 0   
    for iter in range(0,N):
        tf_c = 0
        tf_w = 0
        tf_c = tokens[iter].count(c)
        tf_w = tokens[iter].count(w)
        if tf_c > 0:
           NC = NC+1
        if tf_w >0:
           NW = NW + 1
        co = co + tf_c*tf_w
    idf = min(1,(math.log(N/NC)/math.log(10))/5)
    idfW = min(1,(math.log(N/NW)/math.log(10))/5)
    #print idf
    return (idf,idfW,co)

def coov_builder(concept,query):
    R = len(concept)
    C = len(query)
    delta = 0.1
    coov = np.zeros((R,C))
    conceptList = get_tokens('conRange/list')
   # tokens = [' ' for i in range(0,len(conceptList))]
    tokens = [' ' for i in range(0,4000)]
   # for iter in range(0,len(conceptList)):
    for iter in range(0,4000):
        ####################################add a concept list here
        tokens[iter] = get_tokens('wikiStemed/' + str(iter+1)) 
    for i in range(0,R):  ##R is num of concept
        for j in range(0,C): #num of query terms  
            (idf,idfW,co) = get_idf_co(concept[i],query[j],tokens) 
            #print idf,co         
            coov[i,j] = math.pow((math.log(co+1)/math.log(10)*idf/math.log(10) + delta),idfW)
            #print coov[i,j]
        print i
    return coov 


concept = get_tokens('keys')
query = get_tokens('testStemed/8')

coov = coov_builder(concept,['car','manufact'])
coov1 =np.sort(np.prod(coov,axis = 1))
index = np.argsort(np.sum(coov,axis = 1))
token = get_tokens('keys')

with open('expand','w') as expandWrite:
     for i in range(1,50):
         if coov1[-i]>0:
            expandWrite.write(str(token[index[-i]])+'\t') #for j in range(21-i)]
            print token[index[-i]],coov1[-i]
