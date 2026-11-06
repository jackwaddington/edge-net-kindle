"""
Minimal HTTP server.

GET  /kindle/display.png      → regenerate + serve 600×800 greyscale PNG
"""

from flask import Flask, send_file
from generate import generate
from config import HTTP_PORT

app = Flask(__name__)
PNG_PATH = "/tmp/kindle_display.png"


@app.route("/kindle/display.png")
def display():
    generate(PNG_PATH)
    return send_file(PNG_PATH, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HTTP_PORT)
