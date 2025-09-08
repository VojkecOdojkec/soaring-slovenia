import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"

def wind_temp_profile(lat: float, lon: float, tz: str = "Europe/Ljubljana"):
    """Vrne preprost 'hourly' paket (T na nivojih + veter), dovolj za ocene."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m","dew_point_2m","windspeed_10m","winddirection_10m",
            "temperature_1000hPa","temperature_925hPa","temperature_850hPa",
            "temperature_700hPa","winddirection_925hPa","windspeed_925hPa",
            "winddirection_850hPa","windspeed_850hPa","winddirection_700hPa","windspeed_700hPa"
        ],
        "timezone": tz,
        "models": "icon_seamless"  # stabilen evropski model pri Open-Meteo
    }
    r = requests.get(BASE_URL, params=params, timeout=25)
    r.raise_for_status()
    return r.json()
