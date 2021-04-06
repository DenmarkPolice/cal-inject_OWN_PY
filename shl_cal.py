import requests
import pprint
from bs4 import BeautifulSoup

import os.path
from google_auth_oauthlib.flow import InstalledAppFlow

from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

URL = 'https://www.shl.se/spelschema/SHL_2020_playoff'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
	creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request())
	else:
		flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
		creds = flow.run_local_server(port=0)
	# Save the credentials for the next run
	with open('token.json', 'w') as token:
		token.write(creds.to_json())


results = soup.find_all('div', class_='rmss_c-schedule-game__date-container')
matchups = []
for result in results:

	soup = BeautifulSoup(str(result), 'html.parser')
	date_div = soup.find('div', 'rmss_c-schedule-game__header')
	date = date_div.attrs['data-header-date'] + ''
	time = soup.find('div', 'rmss_c-schedule-game__start-time')
	#print(date)
	#print(time.text)
	teams = soup.find_all('div', 'rmss_c-schedule-game__team-name')
	team_groups = []
	for team in teams:
		if len(team.text) == 3:
			team_groups.append(team.text)
	
	x = 0
	while(len(team_groups) > x):
		matchups.append([team_groups[x], team_groups[x+1], date, time.text])
		x += 2

calendar = GoogleCalendar('')
for matchup in matchups:
	if('FHC' in matchup):
		event = Event(
		'{0} - {1}'.format(matchup[0], matchup[1]),
		start=datetime(2020, 7, 10, 19, 0),
		location='',
		minutes_before_popup_reminder=30
		)
		print(matchup)
		#calendar.add_event(event)