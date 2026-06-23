"""
Task state: tracks last-done timestamps for household tasks.
Persisted as JSON. MQTT logging will update this later.
"""

import json
import os
from datetime import date, datetime
from config import TASKS, TASK_STATE_PATH


def _load() -> dict:
    if os.path.exists(TASK_STATE_PATH):
        with open(TASK_STATE_PATH) as f:
            return json.load(f)
    return {}


def _save(state: dict) -> None:
    with open(TASK_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def mark_done(room: str) -> None:
    state = _load()
    state[room] = date.today().isoformat()
    _save(state)


def get_tasks() -> list[tuple[str, int, bool]]:
    """Return list of (room, days_since, overdue)."""
    state = _load()
    today = date.today()
    result = []
    for room, interval in TASKS:
        last_str = state.get(room)
        if last_str:
            last = date.fromisoformat(last_str)
            days = (today - last).days
        else:
            days = 999  # never done
        overdue = days > interval
        result.append((room, days, overdue))
    return result
