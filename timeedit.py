from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import pandas as pd
import csv
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import date, datetime


SCOPES = ['https://www.googleapis.com/auth/calendar']



def main():

   
    
    ####  GOOGLE CALENDAR AUTHENTIFICATION STUFF

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        print('Connecting with saved credentials')
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Expired credentials, asking user to log in again')
            creds.refresh(Request())
        else:
            print('No credentials found, asking user to log in')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    CAL = build('calendar', 'v3', credentials=creds)

    #Downloading the schedule from TimeEdit
    url = os.getenv('TIMEEDIT_URL')
    
    #Get the csv version of the schedule
    if url.find('.'):
        url = "".join([url.rsplit('.', 1)[0], '.csv'])
        #print(url)
    
    open('schedule.csv', 'wb').write(requests.get(url, allow_redirects=True).content)

    rows = []
    with open('schedule.csv') as f:
        reader = csv.reader(f, quotechar='"')
        for row in reader:
            rows.append(row)
    #print(rows[5])

    calendar = GoogleCalendar(os.getenv('TIMEEDIT_MAIL'))
    
    x = 4
    while(len(rows) > x):
        dates = rows[x][0].split("-")
        start_clock = rows[x][1].split(" ")
        start_clock = start_clock[1].split(":")
        end_clock = rows[x][3].split(" ")
        end_clock = end_clock[1].split(":")
        start = datetime(year=int(dates[0]), month=int(dates[1]), day=int(dates[2]), hour=int(start_clock[0]), minute=int(start_clock[1]))
        end = datetime(year=int(dates[0]), month=int(dates[1]), day=int(dates[2]), hour=int(end_clock[0]), minute=int(end_clock[1]))
        event = Event('{0} {1}'.format(rows[x][5], rows[x][4]),
              start=start,
              end=end)

        calendar.add_event(event)

        print('Attempting to add calendar event')
        x += 1



if __name__ == '__main__':
    main()