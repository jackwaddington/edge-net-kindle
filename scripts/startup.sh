#!/bin/sh
# Kindle startup script — called via @reboot cron entry on boot.
# Cron handles the hourly poll; this script handles boot-time init.

# Guard: crond fires @reboot on every crontab reload, not just real boot.
# /tmp is tmpfs — cleared on boot, so this runs fully once per boot only.
[ -f /var/startup_done ] && exit 0
touch /var/startup_done

DISPLAY_DIR="/mnt/us/kindle"
POLL_SCRIPT="$DISPLAY_DIR/poll.sh"

# Disable screensaver
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Dedicated dashboard: stop the Kindle UI so it doesn't draw menus over it.
# Undo with `/etc/init.d/framework start` or a reboot without this script.
/etc/init.d/framework stop

# Poll on boot, retrying while WiFi comes up: poll.sh exits silently on a
# failed fetch, so a single attempt at boot usually left the old image up.
for i in 1 2 3 4 5 6 7 8 9 10; do
    sh "$POLL_SCRIPT"
    [ "$(find "$DISPLAY_DIR/display.png" -mmin -2 2>/dev/null)" ] && break
    sleep 30
done
