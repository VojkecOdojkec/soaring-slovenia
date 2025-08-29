import os
from datetime import datetime
from app.config import CFG
from app.sites import load_sites
from app.providers.openmeteo import wind_temp_profile
from app.scoring import score_site
from app.summary import build_message
from app.chart import save_minichart
from app.calendar_ics import upsert_daily_event
from app.report import write_report

def estimate_base_top_climb(openmeteo_json):
    h = {1000:110, 925:760, 850:1460, 700:3000}
    hourly = openmeteo_json.get("hourly", {})
    T1000 = hourly.get("temperature_1000hPa", [15])[0]
    T850  = hourly.get("temperature_850hPa",  [5])[0]
    lapse = (T1000 - T850) / ((h[850]-h[1000]) / 1000.0)
    base = 2400 if lapse > 6.5 else 1800
    top  = base + (600 if lapse > 7.5 else 300)
    climb = 3.0 if lapse > 7.0 else 2.0
    return base, top, climb

def build_wind_profile(o):
    hourly = o.get("hourly", {})
    def pick(arr): return arr[0] if isinstance(arr, list) and arr else None
    prof = []
    if hourly.get("winddirection_925hPa") and hourly.get("windspeed_925hPa"):
        prof.append((800,  pick(hourly["winddirection_925hPa"]), pick(hourly["windspeed_925hPa"])))
    if hourly.get("winddirection_850hPa") and hourly.get("windspeed_850hPa"):
        prof.append((1500, pick(hourly["winddirection_850hPa"]), pick(hourly["windspeed_850hPa"])))
    if hourly.get("winddirection_700hPa") and hourly.get("windspeed_700hPa"):
        prof.append((3000, pick(hourly["winddirection_700hPa"]), pick(hourly["windspeed_700hPa"])))
    return prof

def pick_surface_wind(o):
    hourly = o.get("hourly", {})
    d = hourly.get("winddirection_10m", [180])[0]
    s = hourly.get("windspeed_10m", [3.0])[0]
    return d, s

def run_for_today():
    sites = load_sites()
    lat, lon = 46.10, 14.80
    o = wind_temp_profile(lat, lon)
    base, top, climb = estimate_base_top_climb(o)
    wdir, wspd = pick_surface_wind(o)
    wprof = build_wind_profile(o)

    ranked = []
    for s in sites:
        sc = score_site(s, base, top, climb, wdir, wspd)
        ranked.append({**s, "score": sc})
    ranked.sort(key=lambda x: x["score"], reverse=True)

    d_human = datetime.now().strftime("%d.%m.%Y")
    d_iso   = datetime.now().strftime("%Y-%m-%d")
    msg = build_message(d_human, CFG.region, ranked, base, top, climb, wdir, wspd)

    os.makedirs(CFG.chart_dir, exist_ok=True)
    chart_path = os.path.join(CFG.chart_dir, f"chart-{d_human}.png")
    save_minichart(chart_path, base, top, climb,
                   wind_text=f"Veter 10 m: {int(wdir)}° / {wspd:.1f} m/s",
                   wind_profile=wprof, surface=(wdir, wspd))

    repo_slug = os.getenv("GITHUB_REPOSITORY", "VojkecOdojkec/soaring-slovenia")
    branch    = os.getenv("GITHUB_REF_NAME", "main")
    page_url, _site_index = write_report("docs", d_iso, CFG.region, base, top, climb, wdir, wspd, ranked, chart_path, repo_slug, branch)

    chart_fname = os.path.basename(chart_path)
    chart_url = f"https://raw.githubusercontent.com/{repo_slug}/{branch}/charts/{chart_fname}"

    upsert_daily_event(
        CFG.ics_path,
        datetime.now().replace(hour=7, minute=0, second=0, microsecond=0),
        title="Soaring Slovenia – predlog vzletišč",
        description=msg,
        page_url=page_url,
        chart_url=chart_url,
    )

    print("Poročilo:", page_url)
    print("Graf:", chart_url)
    print("TOP10:", [s["name"] for s in ranked[:10]])

if __name__ == "__main__":
    run_for_today()
