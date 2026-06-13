# Kindle 4 — Jailbreak & Setup

## Device

- **Model**: Kindle 4th gen (K4, 2011) — no touch, no backlight, d-pad + page-turn buttons
- **Firmware**: 4.1.4
- **MobileRead identifier**: D01100

## Jailbreak

The Kindle 4 on firmware 4.x is fully supported. All packages from the [MobileRead wiki — Kindle 4/5 jailbreak thread](https://www.mobileread.com/forums/showthread.php?t=88004).

Steps:

1. Download the jailbreak package for K4 from MobileRead
2. Connect Kindle via USB — copy the `.bin` file to the root of the Kindle drive
3. On device: Menu → Settings → Menu → Update Your Kindle
4. Device restarts — jailbreak installed

## SSH over WiFi

After jailbreak, install **USBNetwork** (also from MobileRead). This enables SSH — first over USB, then over WiFi once configured.

1. Install USBNetwork package (same update method as jailbreak)
2. SSH over USB on `192.168.2.2` initially
3. Configure WiFi credentials on the device
4. SSH over WiFi once connected to Edge-NET AP

Default SSH credentials after USBNetwork install: `root` / `mario` (change immediately).

## Disable Screensaver / Prevent Sleep

```bash
# Disable screensaver via lipc
lipc-set-prop com.lab126.powerd preventScreenSaver 1

# Or set a very long timeout (seconds)
lipc-set-prop com.lab126.powerd screenSaverTimeout 86400
```

To make permanent, add to `/etc/rc.d/` or call from the daemon script on startup.

## Filesystem

The root filesystem is read-only by default. Remount to write:

```bash
mntroot rw
# make changes
mntroot ro
```

For persistent changes (scripts, cron), write to `/mnt/us/` (the user data partition — always writable, survives reboots).

## Cron

```bash
# Add to crontab — runs as root
echo "*/5 * * * * /mnt/us/kindle/poll.sh" >> /etc/crontab
```

## Key Tools

| Tool | What it does |
|------|-------------|
| `eips` | Write text or image to e-ink panel |
| `lipc-set-prop` | Set Kindle system properties (sleep, screensaver, WiFi) |
| `lipc-get-prop` | Read Kindle system properties |
| `mntroot rw/ro` | Remount root filesystem read-write / read-only |

## eips Quick Reference

```bash
# Display an image (PNG, must be 600×800 or match screen res)
eips -g /mnt/us/kindle/display.png

# Clear screen
eips -c

# Print text at row/col
eips 0 0 "hello"
```

Image must be 8-bit greyscale PNG at 600×800 pixels for Kindle 4.

## Button Events (lipc)

Page-turn and d-pad buttons emit lipc events. Listen with:

```bash
lipc-wait-event com.lab126.keypad keypress
```

Use in a background script to trigger MQTT publishes on button press.
