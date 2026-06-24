# Kindle 4 — Jailbreak & Setup

## Device

- **Model**: Kindle 4th gen (K4, 2011) — no touch, no backlight, d-pad + page-turn buttons
- **Firmware**: 4.1.4
- **MobileRead identifier**: D01100
- **WiFi IP**: 192.168.0.194 (DHCP — check router if it changes)
- **SSH**: `ssh kindle` (alias in ~/.ssh/config, key auth, no password)

## Status

**Complete.** Jailbroken, USBNetwork installed, SSH over WiFi working.

## Jailbreak

Used NiLuJe's K4 jailbreak package from MobileRead.

Files copied to Kindle root via USB:

- `data.tar.gz`
- `ENABLE_DIAGS`
- `diagnostic_logs/` folder

Source: `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Touch/kindle-k4-jailbreak-1.8.N-r18977.tar.xz`

Steps after copying:

1. Eject USB
2. Menu → Settings → Menu → Restart
3. Device boots into diagnostics mode
4. D → R → Q (left on d-pad to confirm)
5. Wait ~20 seconds — "You are Jailbroken" book appears in library

## USBNetwork / SSH

Package: `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Legacy/kindle-usbnetwork-0.57.N-r18979.tar.xz`

Installed via Menu → Settings → Menu → Update Your Kindle.

### Configuration

`/mnt/us/usbnet/etc/config` key settings:

```sh
K3_WIFI="true"
K3_WIFI_SSHD_ONLY="true"
USE_VOLUMD="true"
```

### Auto-start

The init script (`/etc/rc.d/usbnet-init`) checks for `/mnt/us/usbnet/auto`. Create this file to enable auto-start on boot:

```sh
touch /mnt/us/usbnet/auto
```

The package ships with `DISABLED_auto` — renaming it does nothing. You need a file literally called `auto`.

### SSH key auth

Dropbear reads authorized_keys from `/mnt/us/usbnet/etc/authorized_keys` (not `~/.ssh/authorized_keys`):

```sh
cat ~/.ssh/id_ed25519.pub > /Volumes/Kindle/usbnet/etc/authorized_keys
```

### Mac SSH config

```
Host kindle
    HostName 192.168.0.194
    User root
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
```

### macOS note

macOS 12+ dropped RNDIS support — USB ethernet from the Kindle does **not** work. WiFi SSH is the only option.

## Stock firmware fallback

`firmware/Update_stock_4.1.4_fallback.bin` — copy to Kindle root, Menu → Settings → Menu → Update Your Kindle to reflash stock.

To fully revert: Menu → Settings → Reset to Factory Defaults.

## Filesystem

| Path | Description |
| --- | --- |
| `/mnt/us/` | User data partition — always writable, survives reboots. Put everything here. |
| `/` | Root — read-only by default. `mntroot rw` to remount. |
| `/mnt/us/usbnet/` | USBNetwork install |
| `/mnt/us/usbnet/bin/` | Tools: dropbearmulti, evtest, fbink, htop, curl, jq... |

## Screensaver

Disabled at runtime:

```sh
lipc-set-prop com.lab126.powerd preventScreenSaver 1
```

Add to a startup script in `/mnt/us/` to persist across reboots.

## Key Tools

| Tool | What it does |
| --- | --- |
| `eips` | Write text or image to e-ink panel |
| `lipc-set-prop` / `lipc-get-prop` | Kindle system properties (sleep, screensaver, WiFi, battery) |
| `lipc-wait-event` | Block until a lipc event fires (e.g. button presses) |
| `mntroot rw/ro` | Remount root filesystem read-write / read-only |
| `evtest` | Raw input events (buttons, d-pad) — in `/mnt/us/usbnet/bin/` |

## eips Quick Reference

```sh
eips -g /mnt/us/kindle/display.png   # display 600x800 8-bit greyscale PNG
eips -c                               # clear screen
eips 0 0 "hello"                      # print text at row/col
```

## Button Events

```sh
# Via lipc (higher level — fires on key events)
lipc-wait-event com.lab126.keypad keypress

# Via evtest (raw input — use for d-pad navigation)
/mnt/us/usbnet/bin/evtest /dev/input/event0
```

Use in a background loop to trigger MQTT publishes or menu navigation on button press.

## Cron

```sh
echo "*/5 * * * * /mnt/us/kindle/poll.sh" >> /etc/crontab
```
