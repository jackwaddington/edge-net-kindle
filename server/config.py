# Server configuration — edit before deploying

# Location for weather (Open-Meteo)
LAT = 60.1699  # Helsinki
LON = 24.9384

# Tasks: list of (room, interval_days)
# interval_days = how long before a task is considered overdue
TASKS = [
    ("Bathroom",  7),
    ("Bedroom",  14),
    ("Kitchen",   7),
    ("Hallway",  14),
]

# Path to task state JSON (tracks last-done timestamps)
TASK_STATE_PATH = "tasks_state.json"

# MQTT broker — hub home-network IP (bse0 ethernet uplink). TBD once confirmed.
MQTT_HOST = "localhost"
MQTT_PORT = 1883

# HTTP port for this server
HTTP_PORT = 8080
