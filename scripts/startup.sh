#!/bin/sh
# Kindle startup script — place at /mnt/us/kindle/startup.sh
# Called from /etc/rc.d/userscripts.d/ or equivalent on-boot hook.

DISPLAY_DIR="/mnt/us/kindle"
POLL_SCRIPT="$DISPLAY_DIR/poll.sh"

# Disable screensaver
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Install cron job if not already present
CRON_LINE="*/5 * * * * $POLL_SCRIPT"
if ! grep -qF "$POLL_SCRIPT" /etc/crontab 2>/dev/null; then
    echo "$CRON_LINE" >> /etc/crontab
fi

# Start button daemon in background, restart if it dies
while true; do
    sh "$DISPLAY_DIR/buttons.sh"
    sleep 2
done &

# Run poll immediately so display shows on boot
"$POLL_SCRIPT"
