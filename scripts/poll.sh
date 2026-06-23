#!/bin/sh
# Runs on the Kindle via cron. Fetches the latest display image and renders it.

# Update SERVER_IP to match your dashboard server's IP on the local network
SERVER_IP="192.168.0.61"
SERVER_PORT="8080"
DASHBOARD_URL="http://$SERVER_IP:$SERVER_PORT/kindle/display.png"
IMAGE_PATH="/mnt/us/kindle/display.png"

# Fetch image — fail silently (display keeps last image if server unreachable)
wget -q -O "$IMAGE_PATH" "$DASHBOARD_URL" || exit 0

# Render to e-ink
eips -c
eips -g "$IMAGE_PATH"
