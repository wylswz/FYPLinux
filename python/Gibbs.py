import numpy as np
from gensim import corpora, models
import pickle
import parallelLib as par
import multiprocessing as mp
import matplotlib.pyplot as plt
from multiprocessing import Queue
import gensim
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from sklearn.neighbors import LSHForest



def save_model(doc_topic,topic_word,assigned_corpus,dir):
    with open(dir + '/Gibbs_doc_topic.init','w') as writer:
        pickle.dump(doc_topic,writer)
    with open(dir + '/Gibbs_topic_word.init','w') as writer:
        pickle.dump(topic_word,writer)
    with open(dir + '/Gibbs_corpus.init','w') as writer:
        pickle.dump(assigned_corpus,writer)

def read_model(dir):
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


    doc_topic = np.zeros([num_doc,num_topic])
    topic_word = np.zeros([num_topic,num_word])

    for i in range(num_doc):
        for j in range(len(corpus[i])):
            temp_topic = np.random.randint(num_topic)
            corpus[i][j] = corpus[i][j] + (temp_topic,)
            doc_topic[i,temp_topic] += 1
            topic_word[temp_topic,corpus[i][j][0]] += 1
    
    '''
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
    
    '''   

    return corpus,doc_topic,topic_word






def gibbs_sampling(num_topic,alpha,beta,corpus,dictionary,epoches,init_dir=None):

    num_doc = len(corpus)
    num_word = len(dictionary)
    print num_word

    if init_dir == None:
       assigned_corpus, doc_topic, topic_word = init(num_doc,num_word,num_topic,corpus)
       save_model(doc_topic,topic_word,assigned_corpus,'GibbsInit')
    else:
       doc_topic,topic_word,assigned_corpus = read_model(init_dir)

       

   # assigned_corpus, doc_topic, topic_word = init(num_doc,num_word,num_topic,corpus)
   # save_model(doc_topic,topic_word,assigned_corpus,'GibbsInit')


    ll_list = np.array([])
    key_words = []
    for epoch in range(epoches):
        a_1 = []
        print('iteration %d' %epoch)

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
                new_assignment = np.dot(np.arange(num_topic),mult)
                topic_word[new_assignment,word_id] += 1
                doc_topic[doc_id,new_assignment] += 1
                tempTuple = (word_id,assigned_corpus[i][j][1],new_assignment)
                assigned_corpus[i][j] = tempTuple
        for tempiter in range(num_topic):

            b_1 = np.argsort(topic_word[tempiter,:])
            a_1.append(b_1[::-1])

         
        ll=0
        for i in range(len(assigned_corpus)):
            for j in range(len(assigned_corpus[i])):
                ##index assignment
                doc_id = i
                word_id = assigned_corpus[i][j][0]
                topic_id = assigned_corpus[i][j][2]
                ll_A = np.log((doc_topic[doc_id,topic_id] + alpha)/(np.sum(doc_topic,axis=1)[doc_id] + num_topic*alpha))
                ll_B = np.log((topic_word[topic_id,word_id] + beta)/(np.sum(topic_word,axis=1)[topic_id] + num_word*beta))
                ll += ll_A+ll_B
        print ll
        print a_1


        ll_list = np.append(ll_list,ll)
        
        
    plt.plot(np.arange(epoches),ll_list)
    plt.show()
    
    for i in a_1:
        print [dictionary[idx] for idx in i[0:14]]
    return doc_topic,topic_word,assigned_corpus
        
def load_corpus():
    print 'Loading Corpus'
    with  open('corpus.cp','r') as cp_reader:
         corpus = pickle.load(cp_reader)

    with open('dictionary.dc','r') as dic_reader:
        dictionary = pickle.load(dic_reader)  
    return dictionary,corpus 


def get_tokens(dirc):
    with open(dirc,'r') as shakes:
         text = shakes.read()
         tokens = nltk.word_tokenize(text)
         return tokens            

def query(new_doc,doc_topic,topic_word,dictionary,LSH):
    tokens = []
    token = get_tokens(new_doc)
    stopped_tokens = [i for i in token if not i in en_stop]
    p_stemmer = PorterStemmer()
    stemed_tokens = []
    for i in stopped_tokens:
        try:
            temp_token = str(p_stemmer.stem(i))
            stemed_tokens.append(temp_token)
        except IndexError:
            pass
    tokens = stemed_tokens
    new_corpus=dictionary.doc2bow(tokens)
    new_corpus = to_gibbs_corpus([new_corpus])[0] ##convert 
    new_topic_vector = np.zeros(num_topic)
    for t in new_corpus:
        mult_par = topic_word[:,t[0]]
        mult_par = mult_par/np.sum(mult_par)
        new_topic_vector += np.random.multinomial(t[1],mult_par)
    new_topic_vector = new_topic_vector/np.sum(new_topic_vector)
    dist,indices=LSH.kneighbors(new_topic_vector,n_neighbors=20)
    print indices+1





def to_gibbs_corpus(corpus1):
    print 'Converting corpus to Gibbs sampling format'
    corpus = []
    p=0
    for i in corpus1:
        
        B_List = []
        for j in i:
            for counter in range(j[1]):
                B_List.append((j[0],1))
        corpus.append(B_List)

    return corpus




def knn_search(new_topic_vector,doc_topic,LSH):
    dist,indices=LSH.kneighbors(new_topic_vector,n_neighbors=20)
    return indices






if __name__=='__main__':
   en_stop = get_stop_words('en')
   dictionary,corpus1 = load_corpus()
   corpus = to_gibbs_corpus(corpus1)
   num_topic=8
   #doc_topic,topic_word,corpus = gibbs_sampling(num_topic,0.1,0.1,corpus,dictionary,30)#,init_dir='GibbsInit')
   doc_topic,topic_word,corpus = read_model('GibbsModel')
   #save_model(doc_topic,topic_word,corpus,'GibbsModel')
   doc_topic = doc_topic/np.transpose([np.sum(doc_topic,axis = 1)])
   LSH = LSHForest(random_state=42)
   LSH.fit(doc_topic)

   while True:
         try:
             ipt = raw_input('query:')
         except IOError:
             print 'invalid type'
         else:
             if ipt == 'exit()':
                 break
             else:
                 query(ipt,doc_topic,topic_word,dictionary,LSH)
       


