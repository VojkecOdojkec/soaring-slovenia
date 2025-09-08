# app/providers/openmeteo.py
import time
import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def wind_temp_profile(lat, lon, tz="Europe/Ljubljana", attempts=5):
    """
    Povleče napoved Open-Meteo. Vključen je retry (exponential backoff),
    da Action ne pade pri kratkotrajnih napakah (429/5xx/timeout).
    Ob trajnem neuspehu vrne konservativen fallback, da se .ics in graf
    vseeno izdelata.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join([
            "temperature_2m","dew_point_2m","windspeed_10m","winddirection_10m",
            "temperature_1000hPa","temperature_925hPa","temperature_850hPa","temperature_700hPa",
            "winddirection_925hPa","windspeed_925hPa",
            "winddirection_850hPa","windspeed_850hPa",
            "winddirection_700hPa","windspeed_700hPa"
        ]),
        "timezone": tz
    }

    last_err = None
    for i in range(attempts):
        try:
            r = requests.get(BASE_URL, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            last_err = e
            # 429/5xx/timeouts – počakaj in poskusi znova
            time.sleep(min(30, 2**i))

    # ---- Fallback, če API vztrajno ne deluje ----
    print(f"[WARN] Open-Meteo fetch failed after {attempts} attempts: {last_err}")
    return {
        "hourly": {
            "temperature_1000hPa": [16.0],
            "temperature_850hPa": [7.0],
            "temperature_700hPa": [-3.0],
            "winddirection_10m": [180],
            "windspeed_10m": [3.0]
        }
    }
