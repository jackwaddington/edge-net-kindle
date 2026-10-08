#!/bin/sh
# Runs on the Kindle via cron. Fetches the latest display image and renders it.

# nginx-proxy (CT207): its default server path-routes /kindle, /button and
# /tasks to kindle-server on apps-01. The Kindle can't send a Host header,
# so it must use this IP-based route rather than a hostname.
SERVER_IP="192.168.0.57"
SERVER_PORT="80"
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
