import nltk
import math
import string
import argparse
import numpy as np
import multiprocessing as mp
from multiprocessing import Queue
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import parallelLib as par
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

def trainline(taskListTrain,q,id): ##i is the index of article
    print('Worker %d starting' %id)
    taskSize = len(taskListTrain)
    subMatrix = np.zeros([taskSize,len(tokenList)])
    for i in range(taskSize):
        corpus = get_tokens(taskListTrain[i]+1,str(args.dirT)+'/')
        line = np.zeros([1,len(tokenList)])
        for j in range(len(tokenList)):
            a = corpus.count(tokenList[j])
            subMatrix[i,j] = a
    print('Worker %d ending' %id)
    q.put(subMatrix)

def testline(taskListTest,q,id): ##i is the index of article
    print('Worker %d starting' %id)
    taskSize = len(taskListTest)
    subMatrix = np.zeros([taskSize,len(tokenList)])
    for i in range(taskSize):
        corpus = get_tokens(taskListTest[i]+1,str(args.dir)+'/')
        line = np.zeros([1,len(tokenList)])
        for j in range(len(tokenList)):
            a = corpus.count(tokenList[j])
            subMatrix[i,j] = a
    print('Worker %d ending' %id)
    q.put(subMatrix)



def parMatrix():
    taskTrain = range(numOfTrain)
    taskTest = range(numOfTest)
    taskListTrain = par.splitTask(taskTrain,4)
    taskListTest = par.splitTask(taskTest,4)
    queueList = []
    processList = []
    for i in range(numOfCore):
        queueList.append(Queue())
    p1 = mp.Process(target = trainline,args = (taskListTrain[0],queueList[0],1))
    p2 = mp.Process(target = trainline,args = (taskListTrain[1],queueList[1],2))
    p3 = mp.Process(target = trainline,args = (taskListTrain[2],queueList[2],3))
    p4 = mp.Process(target = trainline,args = (taskListTrain[3],queueList[3],4))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    m1=queueList[0].get()
    m2=queueList[1].get()
    m3=queueList[2].get()
    m4=queueList[3].get()
    m=np.concatenate((m1,m2,m3,m4))

    p1 = mp.Process(target = testline,args = (taskListTest[0],queueList[0],1))
    p2 = mp.Process(target = testline,args = (taskListTest[1],queueList[1],2))
    p3 = mp.Process(target = testline,args = (taskListTest[2],queueList[2],3))
    p4 = mp.Process(target = testline,args = (taskListTest[3],queueList[3],4))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    n1=queueList[0].get()
    n2=queueList[1].get()
    n3=queueList[2].get()
    n4=queueList[3].get()
    n=np.concatenate((n1,n2,n3,n4))



    return m,n
        
        



          
if __name__=='__main__':
    print('Gathering terms, please wait......')
    tokenList = []
    with open('keys','r') as kRead:
      tokenList = nltk.word_tokenize(kRead.read())
      print(len(tokenList))
    matrixTrain = np.zeros([numOfTrain,len(tokenList)])
    matrixTest = np.zeros([numOfTest,len(tokenList)])
    matrixTrain, matrixTest =  parMatrix()
    io.savemat('matrix.mat',{'matrixTest':matrixTest,'matrixTrain':matrixTrain})
    print(np.sum(matrixTrain))



  

