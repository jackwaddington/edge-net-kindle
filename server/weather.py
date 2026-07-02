"""
Fetch weather data from Open-Meteo (no API key required).
"""

import urllib.request
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from config import LAT, LON

HELSINKI = ZoneInfo("Europe/Helsinki")

RAIN_THRESHOLD = 40  # % precipitation probability


def _fetch() -> dict:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&hourly=precipitation_probability"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,"
        f"precipitation_sum,sunrise,sunset,uv_index_max,windspeed_10m_max"
        f"&forecast_days=5"
        f"&timezone=auto"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())


def _wmo_symbol(code: int) -> str:
    if code == 0:
        return "Sun"
    if code in (1, 2):
        return "pCld"
    if code == 3:
        return "Cld"
    if code in (45, 48):
        return "Fog"
    if code in (51, 53, 55, 61, 63, 65, 80, 81, 82):
        return "Rain"
    if code in (56, 57, 66, 67, 71, 73, 75, 77, 85, 86):
        return "Snow"
    if code in (95, 96, 99):
        return "Tstm"
    return "?"


def get_rain_warning() -> tuple[bool, str | None]:
    """Return (will_rain, first_rain_time_str) for remaining hours today."""
    try:
        data = _fetch()
    except Exception:
        return False, None

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    probs = hourly.get("precipitation_probability", [])

    now = datetime.now(HELSINKI)
    today = now.date().isoformat()
    now_hhmm = now.strftime("%H:%M")

    for t, p in zip(times, probs):
        if not t.startswith(today):
            continue
        hour = t[11:16]
        if hour < now_hhmm:
            continue
        if p is not None and p >= RAIN_THRESHOLD:
            return True, hour

    return False, None


def get_sun_times() -> tuple[str | None, str | None]:
    """Return (sunrise_hhmm, sunset_hhmm) for today in local time."""
    try:
        data = _fetch()
    except Exception:
        return None, None

    daily = data.get("daily", {})
    sunrises = daily.get("sunrise", [])
    sunsets = daily.get("sunset", [])

    if not sunrises or not sunsets:
        return None, None

    # First entry is today; format is "YYYY-MM-DDTHH:MM"
    rise = sunrises[0][11:16] if sunrises[0] else None
    setting = sunsets[0][11:16] if sunsets[0] else None
    return rise, setting


def get_forecast() -> list[dict]:
    """
    Return 5-day forecast. Each dict has:
      date, day_name, symbol, high, low, precip_mm, uv_max, wind_max
    """
    try:
        data = _fetch()
    except Exception:
        return []

    daily = data.get("daily", {})
    dates   = daily.get("time", [])
    highs   = daily.get("temperature_2m_max", [])
    lows    = daily.get("temperature_2m_min", [])
    codes   = daily.get("weathercode", [])
    precips = daily.get("precipitation_sum", [])
    uvs     = daily.get("uv_index_max", [])
    winds   = daily.get("windspeed_10m_max", [])

    days = []
    for i, d in enumerate(dates):
        dt = datetime.strptime(d, "%Y-%m-%d")
        days.append({
            "date":      d,
            "day_name":  dt.strftime("%a"),   # Mon, Tue …
            "symbol":    _wmo_symbol(codes[i] if i < len(codes) else 0),
            "high":      highs[i]   if i < len(highs)   else None,
            "low":       lows[i]    if i < len(lows)    else None,
            "precip_mm": precips[i] if i < len(precips) else None,
            "uv_max":    uvs[i]     if i < len(uvs)     else None,
            "wind_max":  winds[i]   if i < len(winds)   else None,
        })
    return days


# Back-compat alias used by old generate.py
def get_weather():
    return get_rain_warning()
