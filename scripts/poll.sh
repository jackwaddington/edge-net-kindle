#!/bin/sh
# Runs on the Kindle via cron. Fetches the latest display image and renders it.

DASHBOARD_URL="http://192.168.0.xxx/kindle/display.png"  # update with dashboard server IP
IMAGE_PATH="/mnt/us/kindle/display.png"

# Fetch image
wget -q -O "$IMAGE_PATH" "$DASHBOARD_URL" || exit 1

# Render to e-ink
eips -c
eips -g "$IMAGE_PATH"
