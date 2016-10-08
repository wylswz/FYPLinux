from bs4 import BeautifulSoup
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
    if re.search(r'^http://www.wsj.+?',str(url)):
       return True
    else:
       return False

urlBegin = 'https://www.wsj.com'
urlUnused.add(urlBegin)
urlUnused.add('http://www.wsj.com/articles/the-billionaires-pawn-1475851819')
i=0
r=0
#load url
while r<50:
    tempArticle = ''
    url = urlUnused.pop()
    print url
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
               tempArticle += str(ps.get_text().encode('utf-8'))
               print(ps.get_text())           

           if len(tempArticle) > 1400:
              r += 1
              writer = open('texts/'+str(r),'w')
              writer.write(tempArticle)
              writer.close
     #   if hasChinese(ps.get_text()):
       
     #   else:
              for  link in soup.find_all('a'):
                   newUrl = link.get('href')
                   if isMedium(newUrl):
                  # print(link.get('href'))
                      if newUrl not in urlUsed:
                         urlUnused.add(newUrl)
                   else:
                      print('non medium website')
              




#urlmanager






"""

while i<50:
      i+=1
      soup = BeautifulSoup(getHtml(url),'html.parser')
      for link in soup.find_all('a'):
   # print(link.get('href'))
          LinkN.append(link.get('href') )

   # print(link.get('href'))

      LinkYStringSet.add(url)
      LinkYString = [L for L in LinkYStringSet]
      for element in LinkN:
          if element is not None:
             LinkNStringSet.add(element.decode('gbk','ignore'))
      for element in LinkNStringSet:
          LinkNString.append(element)
      
      while LinkNString[r] in LinkYString:
            r=random.randint(0,len(LinkNString)-1)      
      url=LinkNString[r]

writer = open('url','w')
writer.writelines(LinkNString)
writer.close()

writer = open('urlUsed','w')
writer.writelines(LinkYString)
writer.close()
"""
