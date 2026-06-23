#!/bin/sh
# Kindle startup script — place at /mnt/us/kindle/startup.sh
# Called from /etc/rc.d/userscripts.d/ or equivalent on-boot hook.

DISPLAY_DIR="/mnt/us/kindle"
POLL_SCRIPT="$DISPLAY_DIR/poll.sh"

# Disable screensaver
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Poll loop — runs every 5 minutes in background
while true; do
    sh "$POLL_SCRIPT"
    sleep 300
done &

# Start button daemon in background, restart if it dies
while true; do
    sh "$DISPLAY_DIR/buttons.sh"
    sleep 2
done &

# Run poll immediately so display shows on boot
"$POLL_SCRIPT"
