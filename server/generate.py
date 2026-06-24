"""
Produces a 600x800 greyscale PNG for the Kindle 4 display.
Serve the output via app.py.
"""

from PIL import Image, ImageDraw, ImageFont
from weather import get_weather
from tasks import get_tasks
from water import get_water_temp

WIDTH, HEIGHT = 600, 800
BG = 255
FG = 0
PADDING = 24

# Font paths — adjust if your server uses different TTF locations
def _font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in [
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/Library/Fonts",
        "/System/Library/Fonts/Supplemental",
    ]:
        path = f"{base}/{name}"
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def get_node_health() -> tuple[bool, list[str]]:
    # TODO: query MQTT broker for node heartbeats
    return True, []


def generate(output_path="display.png") -> None:
    img = Image.new("L", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    font_xl     = _font(52, bold=True)
    font_large  = _font(40, bold=True)
    font_medium = _font(32)
    font_small  = _font(22)

    y = PADDING

    # --- Weather ---
    will_rain, rain_time = get_weather()
    if will_rain and rain_time:
        draw.text((PADDING, y), f"Rain at {rain_time}", font=font_xl, fill=FG)
        y += 70

    # --- Water temperature ---
    _, water_temp = get_water_temp()
    if water_temp is not None:
        draw.text((PADDING, y), f"Water {water_temp:.1f}°C", font=font_large, fill=FG)
        y += 56

    # --- Divider ---
    y += 16
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=FG, width=2)
    y += 24

    # --- Tasks ---
    tasks = get_tasks()
    for room, days, overdue in tasks:
        suffix = " !!" if overdue else ""
        days_str = f"{days}d" if days < 999 else "never"
        label = f"{room:<12} {days_str}{suffix}"
        font = _font(32, bold=overdue)
        draw.text((PADDING, y), label, font=font, fill=FG)
        y += 48

    # --- Node health (bottom) ---
    all_ok, down = get_node_health()
    y = HEIGHT - 56
    draw.line([(PADDING, y), (WIDTH - PADDING, y)], fill=FG, width=1)
    y += 12
    if all_ok:
        draw.text((PADDING, y), "All nodes OK", font=font_small, fill=FG)
    else:
        draw.text((PADDING, y), f"Down: {', '.join(down)}", font=font_small, fill=FG)

    img.save(output_path)


if __name__ == "__main__":
    generate()
    print("Generated display.png")
