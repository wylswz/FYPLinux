import nltk
import math
import string
import argparse
import numpy as np
import multiprocessing as mp
from multiprocessing import Queue
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import scipy.io as io

#################add help document and argument here#################
parser = argparse.ArgumentParser(description='I really want to write a clear discription of this program to help users, but you know what, this is a HELP DOCUMENT!!!! If anyone can understand the documentation of software without going to any forums, then that must be bullshit. So, lets talk about how to use this command: #$%^&*(*&^%$#$%^&*(&^%$#$%^&*(&^%$ ')
parser.add_argument('dir',help=' Directory of training texts',type=str)
parser.add_argument('dirT',help=' Directroy of testing texts',type=str)
parser.add_argument('train',help='Number of documents in training sets',type=int)
parser.add_argument('test',help='Number of documents in testing sets',type=int)
args = parser.parse_args()


####################################################################
print args.dir, args.dirT, args.train, args.test

numOfTrain =args.train
numOfTest = args.test
numOfCore = 4

    ##initialize the matrix  

def get_tokens(i,dirc):
    with open(dirc + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens
def get_corpus(i,dirc):
    with open(dirc + str(i),'r') as corpus:
         text = corpus.read()
         return text

def tf_idf(word):
    length = np.zeros((1,numOfTrain))
    occur = np.zeros((1,numOfTrain))        
    P = np.zeros((1,numOfTrain))
    PLOGP = np.zeros((1,numOfTrain))
    for i in range(0,numOfTrain):
        corpus = get_corpus(i+1,str(args.dir)+'/')
        tokens = get_tokens(i+1,str(args.dir)+'/')
        length[0,i] = len(tokens)
        occur[0,i] = corpus.count(word)
        P[0,i] = occur[0,i]/length[0,i]
        PLOGP[0,i] = P[0,i]*np.log2(P[0,i])
    entropy = PLOGP.sum()
    print word
    print entropy

def trainline(i,q): ##i is the index of article
    corpus = get_tokens(i+1,str(args.dir)+'/')
    print('processing training text: ',i+1)
    line = np.zeros([1,len(tokenList)])
    for j in range(len(tokenList)):
        a = corpus.count(tokenList[j])
        line[0,j] = a
    q.put(line)

def testline(i,q):
    corpus = get_tokens(i+1,str(args.dirT)+'/')
    print ('processing testing text: ',i+1)
    line = np.zeros([1,len(tokenList)])
    for j in range(len(tokenList)):
        a = corpus.count(tokenList[j])
        line[0,j] = a
    q.put(line)

def parMatrix():
    batchTrain = numOfTrain/numOfCore
    batchTest = numOfTest/numOfCore
    queueList = []
    processList = []
    for i in range(numOfCore):
        queueList.append(Queue())
    for i in range(batchTrain):
        p1 = mp.Process(target = trainline,args = (i,queueList[0]))
        p2 = mp.Process(target = trainline,args = (i+1*batchTrain,queueList[1]))
        p3 = mp.Process(target = trainline,args = (i+2*batchTrain,queueList[2]))
        p4 = mp.Process(target = trainline,args = (i+3*batchTrain,queueList[3]))
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        matrixTrain[i]=queueList[0].get()
        matrixTrain[i+batchTrain]=queueList[1].get()
        matrixTrain[i+2*batchTrain]=queueList[2].get()
        matrixTrain[i+3*batchTrain]=queueList[3].get()
        



          
if __name__=='__main__':
    print('Gathering terms, please wait......')
    tokenList = []
    with open('keys','r') as kRead:
      tokenList = nltk.word_tokenize(kRead.read())
      print(len(tokenList))
    matrixTrain = np.zeros([numOfTrain,len(tokenList)])
    matrixTest = np.zeros([numOfTest,len(tokenList)])
    parMatrix()
    io.savemat('matrix.mat',{'matrixTest':matrixTest,'matrixTrain':matrixTrain})
    print(np.sum(matrixTrain))



  

