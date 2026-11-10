"""
Produces a 600x800 greyscale PNG for the Kindle 4 display.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
from weather import get_rain_warning, get_sun_times, get_forecast
from water import get_water_temp
from percyos import get_chores, label

HELSINKI = ZoneInfo("Europe/Helsinki")

WIDTH, HEIGHT = 600, 800
BG = 255
FG = 0
GREY = 140
PADDING = 24
COL_W = WIDTH // 5  # 120px per forecast column


def _font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in [
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
    ]:
        try:
            return ImageFont.truetype(f"{base}/{name}", size)
        except OSError:
            continue
    return ImageFont.load_default()


def _center_text(draw, text, font, x, y, width, fill=FG):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (width - tw) // 2, y), text, font=font, fill=fill)


def _fit(draw, text, font, max_w):
    """Trim text with an ellipsis until it fits max_w pixels."""
    if draw.textbbox((0, 0), text, font=font)[2] <= max_w:
        return text
    while text and draw.textbbox((0, 0), text + "…", font=font)[2] > max_w:
        text = text[:-1]
    return text.rstrip() + "…"


def generate(output_path="display.png") -> None:
    img = Image.new("L", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    f_xl     = _font(52, bold=True)
    f_large  = _font(40, bold=True)
    f_medium = _font(30)
    f_small  = _font(22)
    f_tiny   = _font(18)

    y = PADDING

    # --- Header: full date + sunrise/sunset ---
    now = datetime.now(HELSINKI)
    date_str = now.strftime("%A %-d %B")   # "Thursday 3 July"
    draw.text((PADDING, y), date_str, font=f_medium, fill=FG)

    rise, setting = get_sun_times()
    if rise and setting:
        sun_str = f"^ {rise}  v {setting}"
        bbox = draw.textbbox((0, 0), sun_str, font=f_small)
        tw = bbox[2] - bbox[0]
        draw.text((WIDTH - PADDING - tw, y + 5), sun_str, font=f_small, fill=GREY)

    y += 48

    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=GREY, width=1)
    y += 24

    # --- Rain warning ---
    will_rain, rain_time = get_rain_warning()
    if will_rain and rain_time:
        draw.text((PADDING, y), f"Rain at {rain_time}", font=f_xl, fill=FG)
        y += 76
    else:
        draw.text((PADDING, y), "No rain today", font=f_large, fill=GREY)
        y += 64

    # --- Water temperature ---
    _, water_temp = get_water_temp()
    if water_temp is not None:
        draw.text((PADDING, y), f"Water  {water_temp:.1f}°C", font=f_large, fill=FG)
        y += 60

    y += 16
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=GREY, width=1)
    y += 24

    # --- 5-day forecast columns ---
    forecast = get_forecast()
    col_top = y
    col_h = 250

    for i, day in enumerate(forecast[:5]):
        cx = i * COL_W

        if i > 0:
            draw.line([(cx, col_top), (cx, col_top + col_h)], fill=GREY, width=1)

        # day name
        _center_text(draw, day["day_name"], f_medium, cx, col_top + 8, COL_W)

        # weather symbol
        _center_text(draw, day["symbol"], f_small, cx, col_top + 48, COL_W, fill=GREY)

        # high temp
        if day["high"] is not None:
            _center_text(draw, f'{day["high"]:.0f}°', f_large, cx, col_top + 80, COL_W)

        # low temp
        if day["low"] is not None:
            _center_text(draw, f'{day["low"]:.0f}°', f_medium, cx, col_top + 132, COL_W, fill=GREY)

        # precipitation — only show if enough to matter
        if day["precip_mm"] is not None and day["precip_mm"] >= 1.0:
            _center_text(draw, f'{day["precip_mm"]:.0f}mm', f_small, cx, col_top + 178, COL_W, fill=GREY)

    y = col_top + col_h + 16
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=GREY, width=1)
    y += 20

    # --- UV + Wind (from today's forecast) ---
    if forecast:
        today_fc = forecast[0]
        uv = today_fc.get("uv_max")
        wind = today_fc.get("wind_max")
        line_parts = []
        if uv is not None:
            line_parts.append(f"UV {uv:.0f}")
        if wind is not None:
            line_parts.append(f"Wind {wind:.0f} km/h")
        if line_parts:
            draw.text((PADDING, y), "   ".join(line_parts), font=f_large, fill=FG)
            y += 56

    # --- Chores: days until due, soonest first, two columns ---
    chores = get_chores()
    if chores:
        y += 8
        draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=GREY, width=1)
        y += 16
        f_chore_bold = _font(22, bold=True)
        col_w = (WIDTH - 3 * PADDING) // 2
        row_h = 30
        rows = max(0, (HEIGHT - PADDING - 28 - y) // row_h)  # leave room for "updated"
        for i, (name, days) in enumerate(chores[: rows * 2]):
            x = PADDING + (i // rows) * (col_w + PADDING)
            ry = y + (i % rows) * row_h
            due = days is None or days <= 0
            font = f_chore_bold if due else f_small
            fill = FG if due else GREY
            val = label(days)
            tw = draw.textbbox((0, 0), val, font=font)[2]
            name = _fit(draw, name.capitalize(), font, col_w - tw - 12)
            draw.text((x, ry), name, font=font, fill=fill)
            draw.text((x + col_w - tw, ry), val, font=font, fill=fill)

    # --- Updated at (bottom right, absolute) ---
    updated_str = f"updated {now.strftime('%H:%M')}"
    bbox = draw.textbbox((0, 0), updated_str, font=f_tiny)
    tw = bbox[2] - bbox[0]
    draw.text((WIDTH - PADDING - tw, HEIGHT - PADDING - 20), updated_str, font=f_tiny, fill=GREY)

    img.save(output_path)


if __name__ == "__main__":
    generate()
    print("Generated display.png")
