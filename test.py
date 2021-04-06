from beautiful_date import Apr, hours
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
import os
from dotenv import load_dotenv

load_dotenv()

calendar = GoogleCalendar(os.getenv('MAIL'))

start = (22/Apr/2021)[12:00]
end = start + 2 * hours
event = Event('Meeting',
			  start=start,
			  end=end)

calendar.add_event(event)