# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from willie import module
import requests
import urllib2
import os.path

fpath=os.path.realpath(__file__).replace('btn-football.pyc','').replace('btn-football.py','')
execfile(fpath + "btnfootybotdict.py")


def group_list(lst,cnt):
	current_list=lst
	new_list=[current_list[i:i+cnt] for i in range(0, len(current_list), cnt)]
	grouped_list=[]
	for item in new_list:
		newstring=''
		for element in item:
			newstring += element +  " | "
		grouped_list.append(newstring)
	return grouped_list

@module.rule('^!footy')
def get_livescores_matches(bot,trigger):
	query=trigger.replace("!footy ","").lower()
	query=footy_dict_autocorrect(query)
	url="http://www.livescores.com/"
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
	}
	try:
		r=requests.get(url,timeout=15,headers=headers)
	except:
		bot.say("failed to fetch scores,please try again later")
		return
	if r.status_code != 200:
		bot.say("failed to fetch scores,please try again later")
		return
	#search homepage for single match
	match=search_single_match(query,r.text)
	if match:
		bot.say(match)
		return
	#search homepage for league
	matches=search_league_matches(query,r.text)
	if matches:
		for match in matches:
			bot.say(match)
		return
	#if not found, search previous dates for match then league
	#fpath=os.path.realpath(__file__).replace('btn-football.pyc','').replace('btn-football.py','')
	search_order=[3,2,4,5,6,2,1,0]
	for i in search_order:
		f=open(fpath+ "pages/page" + str(i) + ".html",'r').read()
		#search single match
		match=search_single_match(query,f)
		if match:
			bot.say(match)
			return
		#search league matches
		matches=search_league_matches(query,r.text)
		if matches:
			for match in matches:
				bot.say(match)
			return
		#f.close()
	bot.say("no matches found for: " + query)
	return


def search_single_match(query,htmlsrc):
	soup=BeautifulSoup(htmlsrc)
	leagues=soup.findAll('table',{'class':'league-table'})
	#search matches first
	for league in leagues:
		try:
			matches=league.findAll('tr')
		except:
			continue
		for match in matches:
			try:
				match_time=match.find('td',{'class':'fd'}).text.strip()
				home=match.find('td',{'class':'fh'}).text
				away=match.find('td',{'class':'fa'}).text
				score=match.find('td',{'class':'fs'}).text.strip().replace('? - ?','vs.')
				home_lc=home.lower()
				away_lc=away.lower()
				if (query in home_lc) or (query in away_lc):
					output=match_time + " " + home + " " + score + " " + away
					return output
			except:
				continue
	return False
	

def search_league_matches(query,htmlsrc):
	soup=BeautifulSoup(htmlsrc)
	leagues=soup.findAll('table',{'class':'league-table'})
	matchlist=[]
	for league in leagues:
		try:
			leaguename=league.find('span',{'class':'league'}).text.lower()
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
		matchlist=group_list(matchlist,5)
		return matchlist
	else:
		#can't find anything
		return False

@module.rule('^!table')
def get_table(bot,trigger):
	query=trigger.replace("!table ","").lower()
	url=get_livescores_table_url(query)
	if not url:
		bot.say("invalid query")
		return
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
	}
	try:
		r=requests.get(url,timeout=15,headers=headers)
	except:
		bot.say("failed to fetch table,please try again later")
		return
	if r.status_code != 200:
		bot.say("failed to fetch table,please try again later")
		return
	soup=BeautifulSoup(r.text)
	tables=soup.findAll('table',{'class':'league-wc table mtn bbn'})
	html=[]
	for table in tables:
		tr=table.findAll('tr')
		tr=tr[1:]
		html += tr
	teams=[]
	for item in html:
		team_rank=item.find('td',{'class':'num'}).text.strip()
		team_name=item.find('td',{'class':'cty'}).text.strip()
		team_points=item.find('td',{'class':'ls'}).text.strip()
		output=team_rank + "." + team_name + " " + team_points + "pts"
		teams.append(output)
	teams=group_list(teams,5)
	for team in teams:
		bot.say(team)
	return

"""
@module.rule('@matches')
def get_fifa_matches(bot,trigger):
	#return
	query=trigger.replace("@matches ","").lower()
	url=get_fifa_match_url(query)
	if not url:
		bot.say("invalid query")
		return
	try:
		r=requests.get(url,timeout=20)
		#opener = urllib2.build_opener()
                #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                #r = opener.open(url,timeout=10)
	except:
		bot.say("Failed to retrieve matches")
		return
	#check if response is an error page
	response_code=str(r.status_code)
	if response_code != "200":
		bot.say("Failed to retrieve matches")
		return
	soup=BeautifulSoup(r.text)
	#soup=BeautifulSoup(r)
	#get all the matches
	already_played_matches=soup.findAll("div",{"class":"m mc-match-is-result"})
	if not already_played_matches:
		already_played_matches=soup.findAll("div",{"class":"m listener mc-match-is-result"})
	if not already_played_matches:
		already_played_matches=soup.findAll("div",{"class":"m filterable-match listener mc-match-is-result"})		 
	
	to_be_played_matches=soup.findAll("div",{"class":"m mc-match-is-fixture"})
	if not to_be_played_matches:
		to_be_played_matches=soup.findAll("div",{"class":"m listener mc-match-is-fixture"})
	if not to_be_played_matches:
		to_be_played_matches=soup.findAll("div",{"class":"m filterable-match listener mc-match-is-fixture"})	

	fixture_html=already_played_matches + to_be_played_matches	
	
	matches=[]
	#find info in each match and concatenate them as a single string
	for fixture in fixture_html:
		visitor=fixture.find("div",{"class":"t away"}).text
		home=fixture.find("div",{"class":"t home"}).text
		score_time=fixture.find("span",{"class":"s-resText"}).text.strip()
		res_str=home + " " + score_time + " " + visitor
		matches.append(res_str)
	if not matches:
		bot.say("no matches found")
	#group the list of matches 
	matches=group_list(matches,5)
	#print out the list
	for match in matches:
		bot.say(match)

def get_fifa_match_url(query):
        return{
                'epl':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=england-premier-league-2000000000/matches/calendar.html',
                'la liga':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=spain-liga-2000000037/matches/calendar.html',
                'bundesliga':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=germany-bundesliga-2000000019/matches/calendar.html',
                'serie a':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=italy-serie-a-2000000026/matches/calendar.html',
                'ligue 1':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=france-ligue-1-2000000018/matches/calendar.html',
		'spfl':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=scotland-premier-league-2000000001/matches/calendar.html',
		'mls':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=usa-mls-2000000103/matches/calendar.html',
		'eredivisie':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=netherlands-eredivisie-2000000022/index.html',
		'brasileirao':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=brazil-serie-a-2000000078/index.html',
                'allsvenskan':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=sweden-allsvenskan-2000000029/index.html',
		'liga mx':'http://m.fifa.com/world-match-centre/nationalleagues/nationalleague=mexico-1a-division-2000000104/index.html',
		'champions league':'http://m.fifa.com/world-match-centre/uefachampionsleague/'
		}.get(query,False)
"""

def get_livescores_table_url(query):
	return{
                'epl':'http://www.livescores.com/soccer/england/premier-league/',
                'la liga':'http://www.livescores.com/soccer/spain/primera-division/',
                'bundesliga':'http://www.livescores.com/soccer/germany/bundesliga/',
                'serie a':'http://www.livescores.com/soccer/italy/serie-a/',
                'ligue 1':'http://www.livescores.com/soccer/france/ligue-1/',
		'spfl':'http://www.livescores.com/soccer/scotland/premier-league/',
		'mls':'http://www.livescores.com/soccer/usa/mls/',
		'eredivisie':'http://www.livescores.com/soccer/holland/eredivisie/',
		'brasileirao':'http://www.livescores.com/soccer/brazil/serie-a-brasileiro/',
                'allsvenskan':'http://www.livescores.com/soccer/sweden/allsvenskan/',
		'liga mx':'http://www.livescores.com/soccer/mexico/apertura/',
		'liga sagres':'http://www.livescores.com/soccer/portugal/liga-sagres/'
		}.get(query,False)

