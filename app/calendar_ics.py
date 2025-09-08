from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz, uuid

TZ = pytz.timezone("Europe/Ljubljana")

def upsert_daily_event(ics_path: str, local_dt: datetime, title: str,
                       description: str, chart_url: str | None = None):
    """Ustvari en dnevni dogodek in shrani ICS. `chart_url` je neobvezen dodatek v opis."""
    cal = Calendar()
    cal.add("prodid", "-//Soaring Slovenia//")
    cal.add("version", "2.0")

    ev = Event()
    ev.add("uid", str(uuid.uuid4()) + "@soaring-slovenia")
    ev.add("summary", title)
    ev.add("dtstart", TZ.localize(local_dt))
    ev.add("dtend",   TZ.localize(local_dt + timedelta(minutes=10)))

    body = description + (f"\nGraf: {chart_url}" if chart_url else "")
    ev.add("description", body)

    cal.add_component(ev)

    with open(ics_path, "wb") as f:
        f.write(cal.to_ical())
    return ics_path
