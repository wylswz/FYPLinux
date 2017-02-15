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
from nltk.stem import WordNetLemmatizer
from stop_words import get_stop_words
from gensim import corpora, models
from sklearn.neighbors import LSHForest
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS
import matplotlib.pyplot as plt
from scipy.misc import imread

######## add some arguments to the program


def get_tokens(i,dirc):
    with open(dirc + str(i),'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens
def get_tokens_by_dir(dir):
    with open(dir,'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens

def plotCloud():
    while True:
      try:
          ipt = raw_input('Topic:')
      except ImportError:
          print 'invalid type'
      else:
          cloud_word_tuple = LDA.get_topic_terms(ipt,topn=50)
          cloud_word = [str(dictionary[i[0]])+' ' for i in cloud_word_tuple]
          wd={}
          for i in cloud_word_tuple:
              wd[str(dictionary[i[0]])] = i[1] 
          huaji = imread('250px.jpg')
          wc = WordCloud()
          wc.generate_from_frequencies(wd.items())  
          plt.figure()
          plt.imshow(wc)
          plt.axis('off')
          plt.show()
      if ipt == 'exit()':
          break

def startQuery():
    while True:

      try:
          ipt = raw_input('Directory of query:')
      except ImportError:
          print 'invalid type'
      else:
          query = ipt
      if query == 'exit()':
          break

      

    

      print 'loading query...'
      try:
          token = get_tokens_by_dir(query)
      except IOError:
          print 'invalid file name'
      else:
##########################################query preprocessing
           print 'query pre-processing...'
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
######################################################################################
           dictionary_new = corpora.Dictionary(tokens)
           corpus_new = [dictionary_new.doc2bow(text) for text in tokens]
           QUERY_TOPIC = np.zeros([1,num_topic]) ## topic vector for query

           new_topics = LDA[corpus_new]


           for i in new_topics[0]:
               print(i)
               QUERY_TOPIC[0,i[0]] = i[1] ##assign new topics to query doc-topic matrix

           print 'fetching results for you...'
           lshf = LSHForest(random_state=42)
           lshf.fit(DOC_TOPICS) ##fit the local sensitive hash forest with training data POINT_SET
           dist,indices=lshf.kneighbors(QUERY_TOPIC,n_neighbors=20)
           print indices

           

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

def expand(index,query,concept):
    ##index is returned by knn search, query is original query words, concept is keys
    query_stemed = []
    for term in query:
        term = wnl.lemmatize(term)
        term = stem.stem(term)
        query_stemed.append(term) ##preprocess the query
        

    R = len(concept)
    C = len(query)
    N = len(index)
    delta = 0.4
    coov = np.zeros((R,C))
    tokens = [' ' for i in index] ##documents returned before
    temp_counter=0
    for iter in index:
        ####################################add a concept list here
        tokens[temp_counter] = get_tokens_by_dir('wikiStemed/' + str(iter))
        temp_counter = temp_counter+1 
    for i in range(0,R):  ##R is num of concept
        for j in range(0,C): #num of query terms  
            (idf,idfW,co) = get_idf_co(concept[i],query_stemed[j],tokens) 
            #print idf,co         
            coov[i,j] = math.pow((math.log(co+1)/math.log(10)*idf/(math.log(N)/math.log(10)) + delta),idfW)
            #print coov[i,j]
        print i
    print coov
    return coov 
    






if __name__=='__main__':


   stem = PorterStemmer()
   wnl = WordNetLemmatizer()
   GLOBAL_KEYS = get_tokens_by_dir('keys')




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
   #print dictionary
   print('success!')
   doc_topics = LDA.get_document_topics(corpus,minimum_probability=None,minimum_phi_value=None,per_word_topics=False)
   with open('topicConfig.cfg','r') as cfg_reader:
        num_topic = pickle.load(cfg_reader)
   with open('docConfig.cfg','r') as cfg_reader:     
        num_doc = pickle.load(cfg_reader)  ##read number of docs from the config file

   DOC_TOPICS = np.zeros([num_doc,num_topic]) ##document-topic matrix
   print 'setting up LDA model... this may take a few minutes...'
   for i in range(num_doc):
       for t in doc_topics[i]:
           DOC_TOPICS[i,t[0]] = t[1]     ##construct the doc-topic matrix
   while True:
       try:
           ipt = raw_input('Option: 1. plot, 2. query')
       except IOError:
           pass
       else:
           if ipt == 'exit()':
               break
           if ipt == '1':
               plotCloud() 
           else:
               startQuery()
           

                 
   
##process the query

      
    