"""
Minimal HTTP server.

GET  /kindle/display.png      → regenerate + serve 600×800 greyscale PNG
POST /button/<name>           → publish edge-net/kindle/button/<name> to MQTT
POST /tasks/done/<room>       → mark room task done
"""

from flask import Flask, send_file, abort
from generate import generate
from tasks import mark_done
from config import HTTP_PORT, MQTT_HOST, MQTT_PORT
import paho.mqtt.client as mqtt

app = Flask(__name__)
PNG_PATH = "/tmp/kindle_display.png"

VALID_BUTTONS = {
    "up", "down", "left", "right", "select",
    "page_back", "page_fwd", "menu", "back", "home",
}

_mqtt = mqtt.Client()
_mqtt.connect_async(MQTT_HOST, MQTT_PORT)
_mqtt.loop_start()


@app.route("/kindle/display.png")
def display():
    generate(PNG_PATH)
    return send_file(PNG_PATH, mimetype="image/png")


@app.route("/button/<name>", methods=["POST"])
def button(name):
    if name not in VALID_BUTTONS:
        abort(404)
    _mqtt.publish(f"edge-net/kindle/button/{name}", "press")
    return {"ok": True, "button": name}


@app.route("/tasks/done/<room>", methods=["POST"])
def task_done(room):
    from config import TASKS
    valid = {r for r, _ in TASKS}
    if room not in valid:
        abort(404)
    mark_done(room)
    return {"ok": True, "room": room}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HTTP_PORT)
