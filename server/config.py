import os

# Server configuration — override via env vars for containerised deploys;
# defaults below match the values baked in by the LXC deploy for local dev.

# Location for weather (Open-Meteo)
LAT = float(os.environ.get("KINDLE_LAT", "60.1699"))  # Helsinki
LON = float(os.environ.get("KINDLE_LON", "24.9384"))

# Tasks: list of (room, interval_days)
# interval_days = how long before a task is considered overdue
TASKS = [
    ("Bathroom",  7),
    ("Bedroom",  14),
    ("Kitchen",   7),
    ("Hallway",  14),
]

# Path to task state JSON (tracks last-done timestamps)
TASK_STATE_PATH = "/var/lib/kindle-server/tasks_state.json"

# MQTT broker — hub home-network IP (bse0 ethernet uplink)
MQTT_HOST = os.environ.get("MQTT_HOST", "192.168.0.145")
MQTT_PORT = 1883

# HTTP port for this server
HTTP_PORT = 8080

# Data API (GPS/sensor backend). api.home is nginx-proxy's LAN indirection
# to data-api on apps-01 -- data-api no longer runs on its own LXC IP.
DATA_API_BASE = os.environ.get("DATA_API_BASE", "http://api.home")
WATER_SENSOR_ID = "70B3D57050011439"  # Marjaniemi
