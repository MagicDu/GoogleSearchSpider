#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re,random,csv,time,sys

base_url='https://www.google.com'
user_agents=list()

class searchResult(object):
	def __init__(self, newsurl,title,abstract):
		self.newsurl = newsurl
		self.title=title
		self.abstract=abstract

def load_user_agent():
	fp = open('user_agents', 'r')
	line  = fp.readline().strip('\n')
	while(line):
		user_agents.append(line)
		line = fp.readline().strip('\n')
	fp.close()

#提取文章标题
def get_title(url):
	html=requests.get(url).content
	soup=BeautifulSoup(html,'html.parser')
	title=soup.find('title').text
	return title

#提取链接信息
def extractUrl(href):
	url = ''
	pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
	url_match = pattern.search(href)
	if(url_match and url_match.lastindex > 0):
		url = url_match.group(1)
	return url 

#根据链接提取信息
def abstractPages(url):
	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	newslist=list()
	headers={
		'Referer': base_url,
		'Host':'www.google.com',
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	s=requests.session()
	s=BeautifulSoup(s.get(url,headers=headers).content,'html.parser')
	if s.find('div',{'id':'infoDiv'}):
		print('糟糕，被发现惹，换ip吧 QAQ')
		sys.exit()
	else:
		print('开始抓取了----->>>>')
		div=s.find('div',id='search')
		if div!=None:
			divs=div.findAll('div',{'class':'g'})
			if len(divs)>0:
				for d in divs:
					h3=d.find('h3',{'class':'r'})
					if h3==None:
						continue
					link=h3.find('a')
					if link==None:
						continue
					url=link['href']
					newsurl=extractUrl(url)
					#print(newsurl)
					if url=='':
						continue
					title=link.text
					#print(title)
					abstract=d.find('div',{'class':'st'}).text.replace('\r','').replace('\n','').replace('\t','').strip()
					searchresult=searchResult(newsurl,title,abstract)
					newslist.append(searchresult)
					with open('articels.csv','a') as f:
						writer=csv.writer(f)
						writer.writerow((newsurl,title,abstract))
	return newslist


result_per_page=10
def search(keywords,lang='en',num=result_per_page,tbm='nws'):
	if (num%result_per_page)==0:
		pages=num/result_per_page
	else:
		pages=num/result_per_page+1
	for p in range(0,10):
		start=p*result_per_page
		url='%s/search?hl=%s&num=%d&start=%s&q=%s&tbm=%s'%(base_url,lang,result_per_page,start,keywords,tbm)
		print(url)
		abstractPages(url)
		time.sleep(10)

load_user_agent()
search('hello')
