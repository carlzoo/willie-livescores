import livescores-base

class LSBasketball(LSBase):
	def __init__(self):
        super().__init__()
		self.fpath=os.getcwd()
		load_dictionary(fpath+"/dicts/basketball.txt",self.dict)
		load_dictionary(fpath+"/urls/basketball.txt",self.table_urls)

	def process_query(self,query):
		html=super(LSBasketball, self).fetch_page("http://www.livescore.com/basketball/")
		#attempt to search current page first
		match_search=self.search_page(html)
		if not match_search:
			match_search=search_league(html)
		else:
			return match_search
		if match_search:
			return match_search
		#if not found, search previous dates for match then league
		search_order=["3","2","4","5","6","2","1","0"] #must be list of strings for concatenation
		for i in search_order:
			f=open(fpath+ "/pages/page" + i + ".html",'r').read()
			match_search=self.search_page(f)
			if match_search:
				return match_search
			match_search=self.search_league(f)
			if match_search:
				return match_search
		return False #throw exception here
			
	
	def search_page(self,html):
		soup=BeautifulSoup(html)
		leagues=soup.findAll('table',{'class':'league-multi'})
		thelist=[]
		for league in leagues:
			try:
				matches=league.findAll('tr')
				count=len(matches)
			except:
				continue
			for i in range(0,count-1,2):
				try:
					home_team=matches[i].find('td',{'class':'ft'}).text
					away_team=matches[i+1].find('td',{'class':'ft'}).text
					if (query in home_team.lower()) or (query in away_team.lower()): #other searches done only if query matches for faster runtime
						match_time=matches[i].find('td',{'class':'fd'}).text.strip()
						home_score=matches[i].find('td',{'class':'fs'}).text
						away_score=matches[i+1].find('td',{'class':'fs'}).text
						output=match_time + " " + home_team + " " + home_score + "-" + away_score + " " + away_team
						thelist.append(output)
				except:
					continue
		if thelist:
			return thelist
		else:
			return False

	def search_league(self,html):
		soup=BeautifulSoup(html)
		leagues=soup.findAll('table',{'class':'league-multi'})
		matchlist=[]
		for league in leagues:
			try:
				leaguename=league.find('span',{'class':'league'}).text.lower().replace(' - ',' ').replace('::','')
			except:
				continue
			if query in leaguename.lower():
				matchlist_html=league.findAll('tr')
				count=len(matchlist_html)
				for i in range(0,count-1,2):
					try:
						match_time=matchlist_html[i].find('td',{'class':'fd'}).text.strip()
						home_team=matchlist_html[i].find('td',{'class':'ft'}).text
						home_score=matchlist_html[i].find('td',{'class':'fs'}).text
						away_team=matchlist_html[i+1].find('td',{'class':'ft'}).text
						away_score=matchlist_html[i+1].find('td',{'class':'fs'}).text
						output=match_time + " " + home_team + " " + home_score + "-" + away_score + " " + away_team
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
		html=super(LSBasketball, self).fetch_page(url)
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
