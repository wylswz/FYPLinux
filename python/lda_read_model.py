import nltk
import math
import string
import argparse
import numpy as np
import multiprocessing as mp
import gensim
import pickle
from multiprocessing import Queue
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models

def get_tokens(i,dirc):
    with open(dirc + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens
def get_corpus(i,dirc):
    with open(dirc + str(i),'r') as corpus:
         text = corpus.read()
         return text
en_stop = get_stop_words('en')
with  open('corpus.cp','r') as cp_reader:
      print('loading corpus...')
      corpus = pickle.load(cp_reader)
      print('corpus load successfully!')


with open('dictionary.dc','r') as dic_reader:
     print('loading dictionary...')
     dictionary = pickle.load(dic_reader)
     print('dictionary load successfully!')

print('loading LDA model...')
LDA = models.LdaModel.load('model')
print('success!')
doc_topics = LDA.get_document_topics(corpus,minimum_probability=None,minimum_phi_value=None,per_word_topics=False)
num_doc = 3999
num_topic = 10
DOC_TOPICS = np.zeros([num_doc,num_topic]) ##document-topic matrix
for i in range(num_doc):
    for t in doc_topics[i]:
        DOC_TOPICS[i,t[0]] = t[1]

print(DOC_TOPICS)

##process the query
queryid = 4050
token = get_tokens(queryid,'wiki/')
stopped_tokens = [i for i in token if not i in en_stop]
p_stemmer = PorterStemmer()
stemed_tokens = []
for i in stopped_tokens:
    try:
        temp_token = str(p_stemmer.stem(i))
        stemed_tokens.append(temp_token)
    except IndexError:
        pass
tokens = [stemed_tokens]
dictionary_new = corpora.Dictionary(tokens)
corpus_new = [dictionary_new.doc2bow(text) for text in tokens]

QUERY_TOPIC = np.zeros([1,num_topic]) ## topic vector for query

new_topics = LDA[corpus_new]


for i in new_topics[0]:
    print(i)
    QUERY_TOPIC[0,i[0]] = i[1] ##assign new topics to query doc-topic matrix

print(QUERY_TOPIC)
##print(LDA.print_topics(num_topics=10,num_words=10))