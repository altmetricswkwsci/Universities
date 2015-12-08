# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:52:51 2015

@author: rads
"""
# This code retrieves dblp journal names from dblp site http://dblp.uni-trier.de/db/journals/
# There are 100 journals per page. This code retrieves the journal names by crawling through page by page by randomly sleeping in the middle to avoid 404 error
# This code is written as some journal names are not complete and the journal names are present as titles in their respective hyperlinks

import time
import urllib2
import requests
import random
from bs4 import BeautifulSoup


fjournal = open('dblpjournals.txt', 'a')
firstlink = 'http://dblp.uni-trier.de/db/journals/'
#templink = 'http://dblp.uni-trier.de/db/journals/?pos=501'
r = requests.get (firstlink, auth=('user', 'pass'))
data = r.text
soup = BeautifulSoup (data)
count = 0
while (1):
    division = soup.find('div', attrs={'class' : "hide-body"})
    children = division.findChildren()
    achildren = division.find_all('a')
    for child in achildren:
        # print '----'
        if count % 20 == 0  and count != 0:
            randomnumber = random.randint(10,20) * 50
            print randomnumber
            time.sleep(randomnumber)
        if child.contents[0].find('...') > 0:
            hreflink = child.get('href')        
           
            soup1 = BeautifulSoup(urllib2.urlopen(hreflink))
            
            print soup1.title.string
            fjournal.write('%s\n' %(soup1.title.string.encode('utf-8', 'ignore')))
            count = count + 1
        else:
            print child.contents[0]
            fjournal.write('%s\n' %(child.contents[0].encode('utf-8', 'ignore')))
            count = count + 1
            
    soup = BeautifulSoup(data)
    for a in soup.find_all('a', href=True):
        #print a['href']
        if a['href'].find('?pos=') >= 0 and a.contents[0].find('next') >= 0:
            print "Found the URL:", a['href']
            fjournal.write('%s\n'%(firstlink+a['href']))
            r = requests.get(firstlink + a['href'], auth=('user', 'pass'))
            data = r.text
            if data != None:
                soup = BeautifulSoup(data)
    if data == None:
        print 'no further data'
        break
        
fjournal.close()
