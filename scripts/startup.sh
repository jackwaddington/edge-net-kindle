#!/bin/sh
# Kindle startup script — called via @reboot cron entry on boot.
# Cron handles the hourly poll; this script handles boot-time init and button daemon.

DISPLAY_DIR="/mnt/us/kindle"
POLL_SCRIPT="$DISPLAY_DIR/poll.sh"
BUTTONS_SCRIPT="$DISPLAY_DIR/buttons.sh"
BUTTONS_PID="/tmp/buttons.pid"

# Disable screensaver
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Button daemon — nohup so it survives the calling session ending
if [ -f "$BUTTONS_PID" ] && kill -0 "$(cat $BUTTONS_PID)" 2>/dev/null; then
    : # already running
else
    nohup sh -c "while true; do sh $BUTTONS_SCRIPT; sleep 2; done" \
        > /tmp/buttons.log 2>&1 &
    echo $! > "$BUTTONS_PID"
fi

# Poll immediately on boot (cron handles hourly after this)
sh "$POLL_SCRIPT"
