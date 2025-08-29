from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
import pytz, uuid

TZ = pytz.timezone("Europe/Ljubljana")

def upsert_daily_event(ics_path, local_dt, title, description, chart_url=None):
    cal = Calendar()
    cal.add("prodid", "-//Soaring Slovenia//")
    cal.add("version", "2.0")

    ev = Event()
    ev.add("uid", f"{uuid.uuid4()}@soaring-slovenia")
    ev.add("summary", vText(title))
    ev.add("dtstart", TZ.localize(local_dt))
    ev.add("dtend", TZ.localize(local_dt + timedelta(minutes=10)))

    body = description
    if chart_url:
        # v opis dodamo klikljiv URL
        body += f"\nGraf: {chart_url}"
        # polje URL
        ev.add("url", chart_url)
        # polje ATTACH kot PNG
        ev.add("attach", chart_url, parameters={"FMTTYPE": "image/png"})

    ev.add("description", vText(body))
    cal.add_component(ev)

    with open(ics_path, "wb") as f:
        f.write(cal.to_ical())
    return ics_path
