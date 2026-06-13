# Display Design

## Principle: Peace vs Signal

Most of the time the display is calm. One glance tells you nothing needs attention. When something does need attention it's visible at the corner of your eye — you notice without having to look for it.

This means strong visual hierarchy. Not a dashboard that shows everything all the time (you stop seeing those). A display with a clear resting state that changes meaningfully when something changes.

## Screen

Kindle 4 e-ink panel: **600×800 pixels, 8-bit greyscale**. No backlight. Ideal for a fixed-position ambient display — readable in daylight, draws no power when static.

## Layout (draft)

```
┌─────────────────────────┐
│                         │
│   ☁  Rain at 14:00      │  ← weather signal (large, top)
│                         │
│─────────────────────────│
│                         │
│   Bathroom   3 days     │  ← task states (medium)
│   Bedroom    11 days !! │  ← overdue = !! marker
│                         │
│─────────────────────────│
│                         │
│   All nodes OK          │  ← network status (small, bottom)
│                         │
└─────────────────────────┘
```

**Peace state** (nothing to flag):
- Weather: no rain expected → blank or a small clear-sky icon
- Tasks: all within interval → show nothing, or just the room names with no marker
- Network: all nodes OK → single small line at bottom

**Signal state** (something needs attention):
- Rain incoming → large text, time of expected rain, top of screen
- Task overdue → room name + days, `!!` marker
- Node down → node name at bottom

## What It Shows

### Weather
- Is it going to rain today? If yes: when?
- Source: a weather API called by the dashboard server (not the Kindle directly)
- Display: only shown if rain is expected within the day. Silent otherwise.

### Household Tasks
- Time since each tracked task was last logged
- Tasks defined in the database — rooms, task type, expected interval
- Overdue = past the defined interval → surfaced on display
- Logged via MQTT button press from another Edge-NET node (Keybow, control panel)

### Network
- Edge-NET node health — which nodes are reachable via MQTT heartbeat
- One line, small, bottom of screen. Only calls attention if a node is missing.

## Image Generation

The dashboard server (in `server/`) generates a 600×800 greyscale PNG using Python + Pillow. The Kindle polls this endpoint and renders it with `eips`.

Refresh: every 5 minutes via cron. E-ink handles infrequent refresh fine; more than once a minute causes visible ghosting on the K4.

## Fonts

Use a clean, large sans-serif. Pillow's `ImageFont` with a TTF — something like [Inter](https://rsms.me/inter/) or [IBM Plex Sans](https://www.ibm.com/plex/) works well at e-ink resolution. Avoid thin weights — e-ink contrast isn't like LCD.
