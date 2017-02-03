'''
This program is used to train an LDA model an save the model to file
'''


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

tokens = []

with  open('corpus.cp','r') as cp_reader:
      corpus = pickle.load(cp_reader)

with open('dictionary.dc','r') as dic_reader:
     dictionary = pickle.load(dic_reader)

#dictionary = corpora.Dictionary(tokens)
#corpus = [dictionary.doc2bow(text) for text in tokens] #bow

ldamodel = models.LdaMulticore(corpus,num_topics=10,id2word=dictionary,passes=25,workers=4)
ldamodel.save('model')