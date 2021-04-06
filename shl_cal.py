import requests
import pprint
from bs4 import BeautifulSoup
import os
from datetime import date, datetime

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

URL = 'https://www.shl.se/spelschema/SHL_2020_playoff'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all('div', class_='rmss_c-schedule-game__date-container')
matchups = []
for result in results:
	soup = BeautifulSoup(str(result), 'html.parser')
	date_div = soup.find('div', 'rmss_c-schedule-game__header')
	date = date_div.attrs['data-header-date'] + ''
	time = soup.find('div', 'rmss_c-schedule-game__start-time')
	teams = soup.find_all('div', 'rmss_c-schedule-game__team-name')
	team_groups = []
	for team in teams:
		if len(team.text) == 3:
			team_groups.append(team.text)
	
	x = 0
	while(len(team_groups) > x):
		if time is not None:
			matchups.append([team_groups[x], team_groups[x+1], date, time.text])
		x += 2

calendar = GoogleCalendar(os.getenv('HOCKEY_MAIL'))
for matchup in matchups:
	if('FHC' in matchup):
		dates = matchup[2].split('-')
		clock = matchup[3].split(':')
		start = datetime(year=int(dates[0]), 
							month=int(dates[1]), 
							day=int(dates[2]), 
							hour=int(clock[0]), 
							minute=int(clock[1]))

		end = datetime(year=int(dates[0]), 
							month=int(dates[1]), 
							day=int(dates[2]), 
							hour=int(clock[0])+2, 
							minute=int(clock[1]))

		event = Event('{0} - {1}'.format(matchup[0], matchup[1]),
			  start=start,
			  end=end)

		calendar.add_event(event)