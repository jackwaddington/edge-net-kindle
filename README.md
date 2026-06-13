# edge-net-kindle

Jailbroken Kindle 4 as an ambient e-ink display node on [Edge-NET](https://github.com/jackwaddington/edge-net).

## Hardware

| Part | Detail |
|------|--------|
| Kindle 4th gen | Firmware 4.1.4, no backlight, d-pad + page-turn buttons |
| Connection | WiFi — connects to Edge-NET AP |
| Power | USB (standard Kindle cable) |

## Concept

Most of the time: peace. A calm, readable display that asks nothing of you. At a glance you know nothing needs attention.

When something is up — rain incoming, a task overdue, a node down — it shows at the corner of your eye without you having to go looking. The display escalates only when it matters.

The Kindle's physical buttons (page-turn, d-pad) are available as input triggers — for logging household tasks or navigating display modes — but the primary role is ambient output.

## Jailbreak

Kindle 4 (firmware 4.x) is one of the best-supported jailbreak targets. Full instructions in [SETUP.md](SETUP.md).

Key capabilities post-jailbreak:

- SSH over WiFi
- `eips` — writes text or images directly to the e-ink panel
- `lipc` — Kindle's internal IPC: controls sleep, screensaver, WiFi, battery state
- Python runtime
- Physical buttons available via lipc or evdev

## Display

A Python service on the home network generates a PNG and serves it over HTTP. The Kindle polls it on a cron job and renders it with `eips -g image.png`.

See [DISPLAY.md](DISPLAY.md) for what it shows and the visual hierarchy.

## Architecture

```
Home network
  └── dashboard server (generates PNG)
        ↑ HTTP poll (cron, every 5 min)
Edge-NET WiFi AP (hub)
  └── Kindle 4
        └── eips → e-ink panel
```

The hub's pf firewall allows the Kindle outbound to the dashboard server only. The Kindle has no other internet access.

## Repo structure

```
scripts/       — push.sh (deploy to Kindle), kindle-daemon.sh (poll + render loop)
server/        — dashboard image generator (Python + Pillow)
SETUP.md       — jailbreak walkthrough, SSH setup, disabling screensaver
DISPLAY.md     — what it shows, visual hierarchy, peace vs signal design
```
