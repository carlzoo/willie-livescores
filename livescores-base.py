import abc
import requests
import os
from bs4 import BeautifulSoup

class LSBase(object):
	__metaclass__=abc.ABCMeta

	def __init__(self):
        self.dict={}
		self.table_urls={}

	def load_dictionary(self,filepath,thedict):
		f=open(filepath,'r')
		for line in dictfile:
			line=line.strip()
			if line =="":
        		continue
			alist = line.split("||")
			try:
				key=alist[0]
				value=alist[1]
				thedict[str(key)]=str(value)
			except:
				#throw exception
			alist=[]
		f.close()

	@abstractmethod
	def fetch_page(self,url):
		try:
			headers = {
    		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
			}
			r=requests.get(url,timeout=15,headers=headers)
		except:
			return False
		finally:
			if r.status_code != 200:
				return False
			return r.text
	
	@abstractmethod	
	def process_query(self,query):
		raise NotImplementedError()
