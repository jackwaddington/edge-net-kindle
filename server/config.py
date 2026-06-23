# Server configuration — edit before deploying

# Location for weather (Open-Meteo)
LAT = 51.5074   # London default — update to your coords
LON = -0.1278

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

# MQTT broker (for button daemon and node health, future use)
MQTT_HOST = "localhost"
MQTT_PORT = 1883

# HTTP port for this server
HTTP_PORT = 8080
