import numpy as np
from gensim import corpora, models
import pickle
import parallelLib as par
import multiprocessing as mp
from multiprocessing import Queue

def save_init_model(doc_topic,topic_word,assigned_corpus,dir):
    with open(dir + '/Gibbs_doc_topic.init','w') as writer:
        pickle.dump(doc_topic,writer)
    with open(dir + '/Gibbs_topic_word.init','w') as writer:
        pickle.dump(topic_word,writer)
    with open(dir + '/Gibbs_corpus.init','w') as writer:
        pickle.dump(assigned_corpus,writer)

def read_init_model(dir):
    with open(dir + '/Gibbs_doc_topic.init','r') as writer:
        doc_topic = pickle.load(writer)

    with open(dir + '/Gibbs_topic_word.init','r') as writer:
        topic_word = pickle.load(writer)

    with open(dir + '/Gibbs_corpus.init','r') as writer:
        corpus = pickle.load(writer)
    
    return doc_topic,topic_word,corpus





def par_count_word(taskList,corpus,num_word,q,id):
    print('Worker %d starting' %id)
    num_task = len(taskList)
    subMatrix = np.zeros([num_task,num_word])
    for i in range(num_task):
        for j in range(num_word):
            TF = [[(x[2]==taskList[i] and x[0]==j) for x in l] for l in corpus]
            subMatrix[i,j] = sum([tf.count(True) for tf in TF])
        print taskList[i]
    q.put(subMatrix)
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


    taskList = par.splitTask(range(num_topic),4)
    p1 = mp.Process(target = par_count_word,args = (taskList[0],corpus,num_word,queueList[0],1))
    p2 = mp.Process(target = par_count_word,args = (taskList[1],corpus,num_word,queueList[1],2))
    p3 = mp.Process(target = par_count_word,args = (taskList[2],corpus,num_word,queueList[2],3))
    p4 = mp.Process(target = par_count_word,args = (taskList[3],corpus,num_word,queueList[3],4))
    p1.start()
    p2.start()
    p3.start()
    p4.start() 
    m_init1 = queueList[0].get()
    m_init2 = queueList[1].get()
    m_init3 = queueList[2].get()
    m_init4 = queueList[3].get()  
    topic_word = np.concatenate((m_init1,m_init2,m_init3,m_init4))    
    
    

    return corpus,doc_topic,topic_word






def gibbs_sampling(num_topic,alpha,beta):

    with  open('corpus.cp','r') as cp_reader:
          corpus = pickle.load(cp_reader)

    with open('dictionary.dc','r') as dic_reader:
         dictionary = pickle.load(dic_reader)
    num_doc = len(corpus)
    num_word = len(dictionary)



   # assigned_corpus, doc_topic, topic_word = init(num_doc,num_word,num_topic,corpus)
   # save_init_model(doc_topic,topic_word,assigned_corpus,'Gibbs')


    doc_topic,topic_word,assigned_corpus = read_init_model('Gibbs')
    key_words = []
    for m in range(20):
        a_1 = []
        print('iteration %d' %m)
        for i in range(len(assigned_corpus)):
            for j in range(len(assigned_corpus[i])):
                ##index assignment
                doc_id = i
                word_id = assigned_corpus[i][j][0]
                topic_id = assigned_corpus[i][j][2]
            ## desampling

                topic_word[topic_id,word_id] -= 1
                doc_topic[doc_id,topic_id] -= 1
                probability = np.zeros(num_topic)
                ##resampling
                doc_likes_topic = (doc_topic[doc_id,:] + alpha)/(np.sum(doc_topic,axis=1)[doc_id] + num_topic*alpha)
                topic_likes_word = (topic_word[:,word_id] + beta)/(np.sum(topic_word,axis=1) + num_word*beta)
                probability = doc_likes_topic*np.transpose(topic_likes_word)
                probability = probability*(1/np.sum(probability))
               # print probability
                mult = np.random.multinomial(1,probability)
                new_assignment = np.dot(np.arange(10),mult)
                topic_word[new_assignment,word_id] += 1
                doc_topic[doc_id,new_assignment] += 1
                tempTuple = (word_id,assigned_corpus[i][j][1],new_assignment)
                assigned_corpus[i][j] = tempTuple
        for tempiter in range(num_topic):

            b_1 = np.argsort(topic_word[tempiter,:])
            a_1.append(b_1[::-1])
        print a_1
    for i in a_1:
        print [dictionary[idx] for idx in i[0:14]]
        
            
    









if __name__=='__main__':
   gibbs_sampling(10,0.1,0.1)