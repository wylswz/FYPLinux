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

for j in range(1,4000):
    token = get_tokens(j,'wiki/')
    stopped_tokens = [i for i in token if not i in en_stop]
    p_stemmer = PorterStemmer()
    stemed_tokens = []
    for i in stopped_tokens:
        try:
            temp_token = str(p_stemmer.stem(i))
            stemed_tokens.append(temp_token)
        except IndexError:
            pass
    tokens.append(stemed_tokens)

dictionary = corpora.Dictionary(tokens)
corpus = [dictionary.doc2bow(text) for text in tokens]

with open('corpus.cp','w') as tk_writter:
     pickle.dump(corpus,tk_writter)
with open('dictionary.dc','w') as dic_writter:
     pickle.dump(dictionary,dic_writter)