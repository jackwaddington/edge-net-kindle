#!/bin/sh
# Kindle startup script — called via @reboot cron entry on boot.
# Cron handles the hourly poll; this script handles boot-time init and button daemon.

# Guard: crond fires @reboot on every crontab reload, not just real boot.
# /tmp is tmpfs — cleared on boot, so this runs fully once per boot only.
[ -f /var/startup_done ] && exit 0
touch /var/startup_done

DISPLAY_DIR="/mnt/us/kindle"
POLL_SCRIPT="$DISPLAY_DIR/poll.sh"
BUTTONS_SCRIPT="$DISPLAY_DIR/buttons.sh"
BUTTONS_PID="/var/buttons.pid"

# Disable screensaver
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Button daemon. The K4's BusyBox has no nohup; started from cron/init there
# is no controlling terminal to hang up on, so a plain background job is enough.
if [ -f "$BUTTONS_PID" ] && kill -0 "$(cat $BUTTONS_PID)" 2>/dev/null; then
    : # already running
else
    sh -c "while true; do sh $BUTTONS_SCRIPT; sleep 2; done" \
        > /var/buttons.log 2>&1 &
    echo $! > "$BUTTONS_PID"
fi

# Poll on boot, retrying while WiFi comes up: poll.sh exits silently on a
# failed fetch, so a single attempt at boot usually left the old image up.
for i in 1 2 3 4 5 6 7 8 9 10; do
    sh "$POLL_SCRIPT"
    [ "$(find "$DISPLAY_DIR/display.png" -mmin -2 2>/dev/null)" ] && break
    sleep 30
done
