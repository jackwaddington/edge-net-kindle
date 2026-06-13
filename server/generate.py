"""
Dashboard image generator.
Produces a 600x800 greyscale PNG for the Kindle 4 display.
Serve the output at an HTTP endpoint the Kindle can poll.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

WIDTH, HEIGHT = 600, 800
BG = 255   # white
FG = 0     # black

# TODO: pull from real sources
def get_weather():
    # Return (will_rain: bool, rain_time: str | None)
    return False, None

def get_tasks():
    # Return list of (room: str, days_since: int, overdue: bool)
    return [
        ("Bathroom", 3, False),
        ("Bedroom",  11, True),
    ]

def get_node_health():
    # Return (all_ok: bool, down_nodes: list[str])
    return True, []


def generate(output_path="display.png"):
    img = Image.new("L", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Fonts — update paths to actual TTF files on the server
    font_large  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    font_small  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    y = 40
    padding = 20

    # --- Weather ---
    will_rain, rain_time = get_weather()
    if will_rain and rain_time:
        draw.text((padding, y), f"Rain at {rain_time}", font=font_large, fill=FG)
        y += 70
    # silence if no rain

    # --- Divider ---
    y += 20
    draw.line([(padding, y), (WIDTH - padding, y)], fill=FG, width=1)
    y += 30

    # --- Tasks ---
    tasks = get_tasks()
    for room, days, overdue in tasks:
        marker = " !!" if overdue else ""
        label = f"{room:<12}{days} days{marker}"
        font = font_medium
        draw.text((padding, y), label, font=font, fill=FG)
        y += 50

    # --- Divider ---
    y = HEIGHT - 80
    draw.line([(padding, y), (WIDTH - padding, y)], fill=FG, width=1)
    y += 20

    # --- Node health ---
    all_ok, down = get_node_health()
    if all_ok:
        draw.text((padding, y), "All nodes OK", font=font_small, fill=FG)
    else:
        draw.text((padding, y), f"Down: {', '.join(down)}", font=font_small, fill=FG)

    img.save(output_path)


if __name__ == "__main__":
    generate()
    print("Generated display.png")
