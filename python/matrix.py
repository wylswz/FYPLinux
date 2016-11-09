import nltk
import string
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

def get_tokens(i,dirc):
    with open(dirc + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens
def get_corpus(i,dirc):
    with open(dirc + str(i),'r') as corpus:
         text = corpus.read()
         return text
numOfTrain = 1600
numOfTest = 400


tokenList = []
tokenTupleList = ()
fTrain = open('matrixTrain','w')
fTest = open('matrixTest','w')
print('Gathering terms, please wait......')


for i in range(1,numOfTrain + 1):
    tokens = get_tokens(i,'texts/')
    listTemp = list(enumerate(tokens))
    for term in listTemp:
        if term[1] not in tokenList and len(term[1])>1:
           tokenList.append(term[1])


for i in range(1,numOfTrain + 1):
    corpus = get_corpus(i,'texts/')
    print('processing training text: ',i)
    for j in range(1,len(tokenList)):
        a = corpus.count(tokenList[j])
        fTrain.write(str(a)+'\t')
    fTrain.write('\n')    
 
for i in range(1,numOfTest + 1):
    corpus = get_corpus(i,'textsTEST/')
    print 'processing testing text: ',i
    for j in range(1,len(tokenList)):
        a = corpus.count(tokenList[j])
        fTest.write(str(a)+'\t')
    fTest.write('\n')    

fTrain.close()
fTest.close()
