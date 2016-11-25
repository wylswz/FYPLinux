import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import argparse

parser = argparse.ArgumentParser(description='stem some documents')
parser.add_argument('fromdir',help='from direct',type=str)
parser.add_argument('todir',help='to direct',type=str)
parser.add_argument('number',help='number of documents',type=int)
args = parser.parse_args()

fromDir = args.fromdir + '/'
toDir = args.todir + '/'
number = args.number
def get_tokens(i):
    with open(fromDir + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
    return tokens

stem = PorterStemmer()
wnl = WordNetLemmatizer()
for i in range(1,number+1):
    print 'processing document :',i
    tokens = get_tokens(i)
    listTemp = list(enumerate(tokens))
    for term in listTemp:
        wordLemmatized = wnl.lemmatize(term[1])
        wordStemmed = stem.stem(wordLemmatized)
        with open(toDir + str(i),'a') as writer:
             writer.write(str(wordStemmed)+'\t')
