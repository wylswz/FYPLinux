from bs4 import BeautifulSoup
import urllib
import re
import random
import urllib2






user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
LinkY = [] # These links have been used
LinkN = []
LinkYStringSet = set()
LinkNStringSet = set()
LinkYString=[]
LinkNString=[]
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

url = 'https://medium.com/@108/the-blender-who-would-recite-shakespeare-7a34b1ccf79c#.hjhxsd6tu'
i=0
r=0
values = {'name' : 'WHY','location' : 'SDU','language' : 'Python'}
headers = {'User-Agent' : user_agent}
data = urllib.urlencode(values)

Req = urllib2.Request(url,headers=headers)
Response = urllib2.urlopen(Req)
the_page = Response.read()

soup = BeautifulSoup(the_page,'html.parser')
p=soup.findAll('p')
for ps in p:
    print(ps.get_text())
 #   if hasChinese(ps.get_text()):
       
 #   else:
       


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
