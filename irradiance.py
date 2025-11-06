import requests
from datetime import datetime, timedelta, timezone
from config.load_env import API_KEY
import logging
logger = logging.getLogger(__name__)

def get_uv_forecast_hourly(lat, lon, days=7):
    url = "https://www.meteosource.com/api/v1/flexi/point"
    params = {
        "lat": lat,
        "lon": lon,
        "sections": "hourly",
        "language": "pl",
        "units": "metric",
        "timezone": "Europe/Warsaw",
        "key": API_KEY
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        print("❌ Błąd zapytania:", e)
        return {}

    #cutoff = datetime.now() + timedelta(days=days)  # lokalny czas
    cutoff = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
              + timedelta(days=days)) - timedelta(seconds=1)
    dni = {}
    for entry in data.get("hourly", {}).get("data", []):
        date = datetime.fromisoformat(entry["date"])
        if date > cutoff:
            break
        day_key = date.strftime("%d.%m.%Y")
        hour = date.strftime("%H:%M")

        irradiance = entry.get("irradiance")

        dni.setdefault(day_key, {})[hour] = irradiance

    return dni
