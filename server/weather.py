"""
Fetch today's precipitation forecast from Open-Meteo (no API key required).
Returns (will_rain: bool, rain_time: str | None) where rain_time is like "14:00".
"""

import urllib.request
import json
from datetime import datetime, timezone

# Set your location in config.py
from config import LAT, LON


def get_weather() -> tuple[bool, str | None]:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly=precipitation_probability"
        f"&forecast_days=1"
        f"&timezone=UTC"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception:
        return False, None

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    probs = hourly.get("precipitation_probability", [])

    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    now_hhmm = now.strftime("%H:%M")
    THRESHOLD = 40  # % probability to call it "rain"

    for t, p in zip(times, probs):
        if not t.startswith(today):
            continue
        hour = t[11:16]  # "HH:MM"
        if hour < now_hhmm:  # skip hours already past
            continue
        if p is not None and p >= THRESHOLD:
            return True, hour

    return False, None
