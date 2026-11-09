"""
Fetch household chores from the PercyOS status API.
Returns [(name, days_until | None)], soonest first; [] if unreachable.
days_until <= 0 means due/overdue; None means never done.
"""

import urllib.request
import json

from config import PERCYOS_API_BASE, PERCYOS_API_KEY


def get_chores() -> list[tuple[str, int | None]]:
    if not PERCYOS_API_KEY:
        return []
    req = urllib.request.Request(f"{PERCYOS_API_BASE}/status", headers={"X-API-Key": PERCYOS_API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception:
        return []

    items = next((s["items"] for s in data.get("sections", []) if s.get("topic") == "household_chores"), [])
    chores = [(i["name"], i.get("days_until")) for i in items]
    # never-done (None) sorts first: it's the most overdue
    return sorted(chores, key=lambda c: -10**6 if c[1] is None else c[1])


def label(days: int | None) -> str:
    if days is None:
        return "never"
    if days == 0:
        return "today"
    return f"{days}d" if days > 0 else f"{-days}d late"


assert [label(d) for d in (None, 0, 3, -2)] == ["never", "today", "3d", "2d late"]
