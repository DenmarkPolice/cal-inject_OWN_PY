from __future__ import print_function
import datetime
import os.path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#To download Timeedit csv
import requests
import csv

load_dotenv()  # take environment variables from .env.

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    #Downloading the schedule from TimeEdit
    url = os.getenv('TIMEEDIT_URL')

    if url.find('.'):
        url = "".join([url.rsplit('.', 1)[0], '.csv'])

    open('schedule.csv', 'wb').write(requests.get(url, allow_redirects=True).content)

    rows = []
    with open('schedule.csv') as f:
        reader = csv.reader(f, quotechar='"')
        for row in reader:
            rows.append(row)
    x = 4
    while(len(rows) > x):
        start_time = rows[x][0] + "T" + rows[x][1][1:] + ":00"
        end_time = rows[x][2][1:] + "T" + rows[x][3][1:] + ":00"
        
        event = {
            'summary': rows[x][4],
            'location': rows[x][8],
            'description': rows[x][5],
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Stockholm',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Stockholm',
            },
            'reminders': {
                'useDefault': True
            },
        }

        event = service.events().insert(calendarId=os.getenv('GOOGLE_CALENDAR_SCHOOL_SCHEDULE'), body=event).execute()
        x += 1




if __name__ == '__main__':
    main()