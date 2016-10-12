from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import urllib
import re
import random
import urllib2
user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
urlUsed = set()
urlUnused = set()


def getHtml(url):
    if re.search(r'^http.+?',url):
       print(url)
       print('is valid url')
       opener = urllib.urlopen(url)
       html = opener.read()
       return html
    else:
       print(url)
       print('invalid url!!!!!')
       return('http://www.baidu.com')
def writeUrl(urlList):
    writer = open('url','w')
    writer.writelines(urlList)
    writer.close()

def readUrl(fileName):
    reader = open(fileName,'r')
    readList = reader.readlines()
    reader.close()    
    return readList

def hasChinese(source):
   # temp = source.decode('utf8')
    chineseExpression = ur'[\u4e00-\u9fa5]'
    if re.search(chineseExpression,source):
       return True
    else:
       return False
def isMedium(url):
    print(url)
    try:
        a = re.search(ur'^https://medium.+?',url)
    except UnicodeEncodeError:
           print('encode error')
    else:
           print('encode success')
    if a:
         return True
    else:
         return False


stem = PorterStemmer()
wnl = WordNetLemmatizer()
wordStemed = ''
wordLemmatized = ''
urlBegin = 'https://www.medium.comi'
urlUnused.add(urlBegin)
urlUnused.add('https://medium.com/@LeonXDavis/living-beyond-the-fear-living-beyondthewall-d043abcfe144#.xebvyonmg')
i=0
r=0
#load url
while r<500:
    tempArticle = ''
    url = urlUnused.pop()
   # print url
    if url not in urlUsed:
       headers = {'User-Agent' : user_agent}
       Req = urllib2.Request(url,headers=headers)
       try:
           Response = urllib2.urlopen(Req)

       except urllib2.URLError, e:
              print e


       else:
           urlUsed.add(url)
           the_page = Response.read()
           #url parser
           soup = BeautifulSoup(the_page,'html.parser')
           p=soup.findAll('p')
           for ps in p:
               psStr = str(ps.get_text().encode('utf-8'))
               psStr = re.sub(r'[^a-zA-Z\s\n]',' ',psStr)
               if len(psStr)>2:
                  wordLemmatized = wnl.lemmatize(psStr)
                  wordStemed = stem.stem(wordLemmatized)
                  tempArticle += str(wordStemed)
       #        print(ps.get_text())           

           if len(tempArticle) > 800:
              r += 1
              writer = open('texts/'+str(r),'w')
              writer.write(tempArticle)
              writer.close
     #   if hasChinese(ps.get_text()):
       
     #   else:
              for  link in soup.find_all('a'):
                   newUrl = link.get('href')
                   if newUrl != None and type(newUrl) == type(u"") and newUrl.find(u'\u2019') >= 0:
                      newUrl = newUrl.replace(u'\u2019', '\'')
                   try:
                       tempStr = str(newUrl)
                   except UnicodeEncodeError:
                          pass
                   else:
                        if isMedium(tempStr):
                  # print(link.get('href'))
                           if newUrl not in urlUsed:
                              urlUnused.add(newUrl)
         #          else:
        #              print('non medium website')
              




#urlmanager






"""

"""
