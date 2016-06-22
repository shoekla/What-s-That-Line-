import time
import requests
import string
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import re
from random import randint
def is_in_arr(lis,s):
	result=False
	for item in lis:
		if item==s:
			result=True
	return result
def deleteDuplicates(lis):
	newLis=[]
	for item in lis:
		if item not in newLis:
			newLis.append(item)
	return newLis

def getGoodLink(url):
	k = url.rfind("/")
	return url[:k+1]
def crawl(url,pages):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "microsoft" not in href_test and "facebook" not in href_test and "twitter" not in href_test:
					if href_test.startswith("http"):
						pages.append(str(href))
					else:
						lin=getGoodLink(url)
						pages.append(lin+str(href))

	except:
		print "Error at: "+str(url)
def crawlTitle(url):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('span'):
			try:
				href=link.get('title')
				if href != "Loading icon" and href != None:
					arr.append(href)
				
			except:
				pass
		new = deleteDuplicates(arr)
		return new[0]


	except:
		print "Error at: "+str(url)
#print crawlTitle("https://www.youtube.com/watch?v=ek9fUnnzAhk")
def getPartial(answer,title):
	points=0
	answers = answer.split(" ")
	for item in answers:
		if str(item) in title:
			points= points + 2
	if points > 10:
		return 10		
	return points

def GradeYouQuiz(answer, title):
	points=0
	answer = str(answer).lower()
	title = "https://www.youtube.com/watch?v="+str(title)
	title = crawlTitle(title)
	title = str(title).lower()
	answerStripped = answer.strip()
	titleStripped = title.strip()
	if answerStripped == titleStripped:
		points = 10
	else:
		points = getPartial(answer,title)
	return points
def getBingLink(artist) :
	artist = artist.replace(" ","+")
	result = "http://www.bing.com/search?q="+artist+"&go=Submit&qs=n&form=QBLH&pq="+artist+"&sc=8-10&sp=-1&sk=&cvid=4CA41F960EDF4038AEE79C520BFD8C05"
	return result
def getSongs(artist) :

	try:
		originalA = artist
		artist = artist + " songs"
		url = getBingLink(artist)
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		originalA = originalA.lower()
		originalA = originalA.replace(" ", "+")
		oG = originalA+"+"
		le = len(oG)
		originalA = originalA+"+songs"
		count = 0;
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href).lower()
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(arr,str(href))==False:
					if href_test.startswith("/search"):
						if originalA in href_test:
							if ("&filters" in href_test) :
								count += 1
								href_test = href_test[le+10:href_test.index("&filters")]
								if (count != 1 and count < 15) :
									href_test = href_test.replace("%27","'")
									href_test = href_test.replace("+"," ")
									arr.append(href_test)
									print href_test
		return arr											
						
			

	except Exception,e: print str(e)



def getLyricsLink(songName) :
	try :
		songName = songName.replace(" ","+")
		url = "http://www.bing.com/search?q="+songName+"+lyrics&go=Submit&qs=n&form=QBLH&pq="+songName+"+lyrics&sc=9-17&sp=-1&sk=&ghc=1&cvid=2E43139C36074F0AB1AFCAE5812CE8A0"
		return url
	except Exception,e: print str(e)

def getLyrics(songName) :
	try :
		songLink = getLyricsLink(songName)
		url = songLink
		arr = []
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('p', {"class","b_paractl"}) :
			arr.append(link)
		i = len(arr)
		res = takeoutHTML(arr[randint(0,i-1)])
		print res
		return res
	except Exception,e: print str(e)

def takeoutHTML(lyric) :
	res = ""
	count = 0
	for i in lyric:
		if i == '<':
			count = 1 
		if i == '>':
			count = 2
		if count == 0 :
			if i == '"':
				res = res + "'"
			else :
				res = res + str(i)
		if count == 2 :
			res = res + " "
			count = 0
	res = res.replace("<br/>"," ")
	return res





