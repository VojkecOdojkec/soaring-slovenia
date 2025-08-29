from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
import pytz, uuid

TZ = pytz.timezone("Europe/Ljubljana")

def upsert_daily_event(ics_path, local_dt, title, description, page_url, chart_url):
    cal = Calendar()
    cal.add("prodid", "-//Soaring Slovenia//")
    cal.add("version", "2.0")

    ev = Event()
    ev.add("uid", f"{uuid.uuid4()}@soaring-slovenia")
    ev.add("summary", vText(title))
    ev.add("dtstart", TZ.localize(local_dt))
    ev.add("dtend", TZ.localize(local_dt + timedelta(minutes=10)))

    body = description + f"\nPoročilo: {page_url}\nGraf: {chart_url}"
    ev.add("description", vText(body))
    ev.add("url", page_url)  # klik v koledarju
    ev.add("attach", chart_url, parameters={"FMTTYPE": "image/png"})  # priponka

    cal.add_component(ev)
    with open(ics_path, "wb") as f:
        f.write(cal.to_ical())
    return ics_path
