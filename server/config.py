import os

# Server configuration — override via env vars for containerised deploys;
# defaults below match the values baked in by the LXC deploy for local dev.

# Location for weather (Open-Meteo)
LAT = float(os.environ.get("KINDLE_LAT", "60.1699"))  # Helsinki
LON = float(os.environ.get("KINDLE_LON", "24.9384"))

# PercyOS status API (household chores). In-cluster service name on k3s;
# the key is the same PERCYOS_API_KEY PercyOS checks. Empty key = no chores block.
PERCYOS_API_BASE = os.environ.get("PERCYOS_API_BASE", "http://percyos-api:8001")
PERCYOS_API_KEY = os.environ.get("PERCYOS_API_KEY", "")

# HTTP port for this server
HTTP_PORT = 8080

# Data API (GPS/sensor backend). api.home is nginx-proxy's LAN indirection
# to data-api on apps-01 -- data-api no longer runs on its own LXC IP.
DATA_API_BASE = os.environ.get("DATA_API_BASE", "http://api.home")
WATER_SENSOR_ID = "70B3D57050011439"  # Marjaniemi
