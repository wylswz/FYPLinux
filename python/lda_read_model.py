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

def plotTopic():
    num_words=10
    while True:
      try:
          ipt = raw_input('Topic:')
      except ImportError:
          print 'invalid type'
      else:
          
          if ipt == 'exit()':
               break
          tpc_idx=int(ipt)-1
          if tpc_idx > num_words-1:
              print 'Topic index too large'
          else:
               
               prob_list=np.zeros(num_words)
               index = np.arange(num_words)
               bar_width = 0.3
               wordList = []
               word_tuple = LDA.get_topic_terms(tpc_idx,topn=num_words)
               print word_tuple
               j=0
               for i in word_tuple:
                   prob_list[j] = i[1]
                   j=j+1
               for i in range(num_words):
                   wordList.append(str(dictionary[word_tuple[i][0]]))
               plt.bar(index,prob_list,bar_width) 
               plt.xticks(index + bar_width / 2, wordList)

               plt.show()
 


def plotTopicProp():
    pass
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
           ipt = raw_input('Option: 1. plotCloud, 2. query, 3. plotTopic')
       except IOError:
           pass
       else:
           if ipt == 'exit()':
               break
           if ipt == '1' or ipt == 'plotCloud':
               plotCloud() 
           if ipt == '2' or ipt == 'query':
               startQuery()
           if ipt == '3' or ipt == 'plotTopic':
               plotTopic()
           else:
               pass

                 
   
##process the query

      
    