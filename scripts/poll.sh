#!/bin/sh
# Runs on the Kindle via cron. Fetches the latest display image and renders it.

# Update SERVER_IP to match your dashboard server's IP on the local network
SERVER_IP="192.168.0.62"
SERVER_PORT="8080"
DASHBOARD_URL="http://$SERVER_IP:$SERVER_PORT/kindle/display.png"
IMAGE_PATH="/mnt/us/kindle/display.png"

EIPS=/usr/sbin/eips
TMP_PATH="${IMAGE_PATH}.tmp"

# Fetch image — fail silently (display keeps last image if server unreachable)
wget -q -O "$TMP_PATH" "$DASHBOARD_URL" || exit 0
mv "$TMP_PATH" "$IMAGE_PATH"

# Render to e-ink
$EIPS -c
$EIPS -g "$IMAGE_PATH"
