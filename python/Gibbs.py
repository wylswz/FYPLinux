import numpy as np
from gensim import corpora, models
import pickle
import parallelLib as par
import multiprocessing as mp
from multiprocessing import Queue


def par_count_word(taskList,corpus,num_topic,num_word,q):


    pass



def init(num_doc,num_word,num_topic,corpus): ##initialize assignment


    processList = []
    queueList = []
    for i in range(4):
        queueList.append(Queue())
    #parallel computing initialization



    for i in range(num_doc):
        for j in range(len(corpus[i])):
            corpus[i][j] = corpus[i][j] + (np.random.randint(num_topic),)
    doc_topic = np.zeros([num_doc,num_topic])
    topic_word = np.zeros([num_topic,num_word])

    for i in range(num_doc):
        for j in range(num_topic):
            doc_topic[i,j] = sum([x[2]==j for x in corpus[i]])


    taskList = par.splitTask(num_topic,4)

    #for i in range(num_topic):
    #    for j in range(num_word):
    #        TF = [[(x[2]==i and x[0]==j) for x in l] for l in corpus]
    #        topic_word[i,j] = sum([tf.count(True) for tf in TF])
    #        print j

    return corpus




def gibbs_sampling(num_topic):
    with  open('corpus.cp','r') as cp_reader:
          corpus = pickle.load(cp_reader)

    with open('dictionary.dc','r') as dic_reader:
         dictionary = pickle.load(dic_reader)
    num_doc = len(corpus)
    num_word = len(dictionary)
    
    assigned_corpus = init(num_doc,num_word,num_topic,corpus)
    #print sum([x[2]==1 for x in assigned_corpus[0]])
    m = [[(x[2]==3 and x[0]==400) for x in l] for l in assigned_corpus]
    

gibbs_sampling(10)