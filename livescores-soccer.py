import livescores-base

class LSSoccer(LSBase):
	def __init__(self):
        super().__init__()
		self.fpath=os.getcwd()
		load_dictionary(fpath+"/dicts/soccer.txt",self.dict)
		load_dictionary(fpath+"/urls/soccer.txt",self.table_urls)

	def autocorrect(self,t):
		return self.dict.get(t,t)

	def process_query(self,query):
		q=autocorrect(query)
		html=super(LSSocer, self).fetch_page("http://livescore.com")
		#attempt to search current page first
		match_search=self.search_page(html,q)
		if not match_search:
			match_search=search_league(html,q)
		else:
			return match_search
		if match_search:
			return match_search
		#if not found, search previous dates for match then league
		search_order=["3","2","4","5","6","2","1","0"] #must be list of strings for concatenation
		for i in search_order:
			f=open(fpath+ "/pages/page" + i + ".html",'r').read()
			match_search=self.search_page(f,q)
			if match_search:
				return match_search
			match_search=self.search_league(f,q)
			if match_search:
				return match_search
		return False
			
	
	def search_page(self,html,query):
		soup=BeautifulSoup(html)
		leagues=soup.findAll('table',{'class':'league-table'})
		thelist=[]
		for league in leagues:
			try:
				matches=league.findAll('tr')
			except:
				continue
			for match in matches:
				try:
					home=match.find('td',{'class':'fh'}).text
					away=match.find('td',{'class':'fa'}).text
					if (query in home.lower()) or (query in away.lower()): #other searches done only if query matches for faster runtime
						match_time=match.find('td',{'class':'fd'}).text.strip()
						score=match.find('td',{'class':'fs'}).text.strip().replace('? - ?','vs.')
						output=match_time + " " + home + " " + score + " " + away
						thelist.append(output)
				except:
					continue
		if thelist:
			return thelist
		else:
			return False

	def search_league(self,html.query):
		soup=BeautifulSoup(html)
		leagues=soup.findAll('table',{'class':'league-table'})
		matchlist=[]
		for league in leagues:
			try:
				leaguename=league.find('span',{'class':'league'}).text.lower().replace(' - ',' ').replace('::','')
			except:
				continue
			if query in leaguename.lower():
				matchlist_html=league.findAll('tr')
				for item in matchlist_html:
					try:
						match_time=item.find('td',{'class':'fd'}).text.strip()
						home=item.find('td',{'class':'fh'}).text
						away=item.find('td',{'class':'fa'}).text
						score=item.find('td',{'class':'fs'}).text.strip().replace('? - ?','vs.')
						output=match_time + " " + home + " " + score + " " + away
						matchlist.append(output)
					except:
						continue
		if matchlist:
			return matchlist
		else:
			#can't find anything
			return False

	def get_table(self,query):
		url=
		if not url:
			return False #error handling goes here
		html=super(LSSocer, self).fetch_page(url)
		soup=BeautifulSoup(html)
		tables=soup.findAll('table',{'class':'league-wc table mtn bbn'})
		rows=[]
		for table in tables:
			tr=table.findAll('tr')
			tr=tr[1:]
			rows += tr
		teams=[]
		for item in rows:
			team_rank=item.find('td',{'class':'num'}).text.strip()
			team_name=item.find('td',{'class':'cty'}).text.strip()
			team_points=item.find('td',{'class':'ls'}).text.strip()
			output=team_rank + "." + team_name + " " + team_points + "pts"
			teams.append(output)
		return teams
