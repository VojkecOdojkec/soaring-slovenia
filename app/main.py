import os
from datetime import datetime
from app.config import CFG
from app.sites import load_sites
from app.providers.openmeteo import wind_temp_profile
from app.scoring import score_site
from app.summary import build_message
from app.chart import save_minichart
from app.calendar_ics import upsert_daily_event

def estimate_base_top_climb(openmeteo_json):
    h = {1000:110, 925:760, 850:1460, 700:3000}
    hourly = openmeteo_json.get('hourly', {})
    T1000 = (hourly.get('temperature_1000hPa') or [15])[0]
    T850  = (hourly.get('temperature_850hPa')  or [5])[0]
    lapse = (T1000 - T850) / ((h[850]-h[1000])/1000)
    base = 2400 if lapse > 6.5 else 1800
    top  = base + (600 if lapse > 7.5 else 300)
    climb = 3.0 if lapse > 7.0 else 2.0
    return base, top, climb

def pick_wind(openmeteo_json):
    hourly = openmeteo_json.get('hourly', {})
    dir10 = (hourly.get('winddirection_10m') or [180])[0]
    spd10 = (hourly.get('windspeed_10m')    or [3.0])[0]
    return dir10, spd10

def run_for_today():
    sites = load_sites()
    lat, lon = 46.56, 15.65  # center Vzhodne Štajerske (Maribor)
    o = wind_temp_profile(lat, lon)
    base, top, climb = estimate_base_top_climb(o)
    wdir, wspd = pick_wind(o)

    ranked = []
    for s in sites:
        sc = score_site(s, base, top, climb, wdir, wspd)
        ranked.append({**s, 'score': sc})
    ranked.sort(key=lambda x: x['score'], reverse=True)

    today = datetime.now().strftime('%d.%m.%Y')
    msg = build_message(today, 'Slovenija', ranked, base, top, climb, wdir, wspd)

    os.makedirs(CFG.chart_dir, exist_ok=True)
    chart_path = os.path.join(CFG.chart_dir, f'chart-{today}.png')
    save_minichart(chart_path, base, top, climb, f'Veter: {int(wdir)}° / {wspd:.1f} m/s')

    upsert_daily_event(CFG.ics_path, datetime.now().replace(hour=7, minute=0, second=0, microsecond=0),
                       title='Soaring Slovenia – predlog vzletišč',
                       description=msg,
                       chart_url=os.path.abspath(chart_path))

    print(msg)
    print('Chart:', os.path.abspath(chart_path))
    print('ICS:', os.path.abspath(CFG.ics_path))

if __name__ == '__main__':
    run_for_today()
