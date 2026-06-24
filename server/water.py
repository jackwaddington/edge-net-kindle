"""
Fetch the latest swimming water temperature from the data API.
Returns (name: str | None, temp_water: float | None).
"""

import urllib.request
import json

from config import DATA_API_BASE, WATER_SENSOR_ID


def get_water_temp() -> tuple[str | None, float | None]:
    url = f"{DATA_API_BASE}/water/latest"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception:
        return None, None

    if not isinstance(data, list) or not data:
        return None, None

    entry = next((x for x in data if x.get("dev_id") == WATER_SENSOR_ID), data[0])
    name = entry.get("name")
    temp = entry.get("temp_water")
    if temp is None:
        return None, None
    return name, float(temp)
