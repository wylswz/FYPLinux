import nltk
import string
import argparse
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

#################add help document and argument here#################
parser = argparse.ArgumentParser(description='I really want to write a clear discription of this program to help users, but you know what, this is a HELP DOCUMENT!!!! If anyone can understand the documentation of software without going to any forums, then that must be bullshit. So, lets talk about how to use this command: #$%^&*(*&^%$#$%^&*(&^%$#$%^&*(&^%$ ')
parser.add_argument('dir',help=' Directory of training texts',type=str)
parser.add_argument('dirT',help=' Directroy of testing texts',type=str)
parser.add_argument('train',help='Number of documents in training sets',type=int)
parser.add_argument('test',help='Number of documents in testing sets',type=int)
args = parser.parse_args()


####################################################################
print args.dir, args.dirT, args.train, args.test



def get_tokens(i,dirc):
    with open(dirc + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens
def get_corpus(i,dirc):
    with open(dirc + str(i),'r') as corpus:
         text = corpus.read()
         return text
numOfTrain =args.train
numOfTest = args.test


tokenList = []
tokenTupleList = ()

print('Gathering terms, please wait......')


for i in range(1,numOfTrain + 1):
    tokens = get_tokens(i,str(args.dir)+'/')
    listTemp = list(enumerate(tokens))
    for term in listTemp:
        if term[1] not in tokenList and len(term[1])>1:
           tokenList.append(term[1])

with open('matrixTrain1','w') as fTrain:
     for i in range(1,numOfTrain + 1):
         corpus = get_corpus(i,str(args.dir)+'/')
         print('processing training text: ',i)
         for j in range(1,len(tokenList)):
             a = corpus.count(tokenList[j])
             fTrain.write(str(a)+'\t')
         fTrain.write('\n')    
with open('matrixTest1','w') as fTest:
     for i in range(1,numOfTest + 1):
         corpus = get_corpus(i,str(args.dirT)+'/')
         print 'processing testing text: ',i
         for j in range(1,len(tokenList)):
             a = corpus.count(tokenList[j])
             fTest.write(str(a)+'\t')
         fTest.write('\n')    

