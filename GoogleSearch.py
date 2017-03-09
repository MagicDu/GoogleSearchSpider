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

#根据链接提取信息
def abstractPages(url):
	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	#print(user_agent)
	newslist=list()
	headers={
		'Referer': base_url,
		'Host':'www.google.com',
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	s=requests.session()
	s=BeautifulSoup(s.get(url,headers=headers).content,'html.parser')
	#print(s)
	if s.find('div',{'id':'infoDiv'}):
		print('糟糕，被发现了，换ip吧')
		sys.exit()
	else:
		news_list=s.findAll('div',{'class','g'})
		for link in news_list:
			href=link.find('a')['href']
			#print(href)
			if re.match('^http',href):
				newsurl=href
				#print(href)
				try:
					title=link.find('a',{'class':'l'}).text
					print(title)
				except Exception as e:
					continue
				abstract=link.find('div',{'class':'st'}).text.replace('\r','').replace('\n','').replace('\t','').strip()
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
		time.sleep(5)

load_user_agent()
search('hello')




