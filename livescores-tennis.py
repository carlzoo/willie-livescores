import livescores-base
from bs4 import BeautifulSoup

class LSTennis(LSBase):
	def fetch_page(self):
		u="http://www.livescore.com/tennis/"
		s = super(LSTennis, self).fetch_page(u)
		return s

	def process_query(self,query):
		html=self.fetch_page()
		#attempt to search single query first
		
		
	
	def search_page(self,html):
		soup=BeautifulSoup(html)
		#to be completed
		if thelist:
			return thelist
		else:
			return False

	def search_table(self,html):
		soup=BeautifulSoup(html)
		#to be completed
		if matchlist:
			return matchlist
		else:
			#can't find anything
			return False
