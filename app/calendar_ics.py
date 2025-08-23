from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz, uuid

TZ = pytz.timezone('Europe/Ljubljana')

def upsert_daily_event(ics_path, local_dt, title, description, chart_url=None):
    cal = Calendar(); cal.add('prodid', '-//Soaring Slovenia//'); cal.add('version', '2.0')
    event = Event(); event.add('uid', str(uuid.uuid4())+'@soaring-slovenia')
    event.add('summary', title)
    event.add('dtstart', TZ.localize(local_dt))
    event.add('dtend', TZ.localize(local_dt + timedelta(minutes=10)))
    body = description + (f"\nGraf: {chart_url}" if chart_url else '')
    event.add('description', body)
    cal.add_component(event)
    with open(ics_path, 'wb') as f: f.write(cal.to_ical())
    return ics_path
