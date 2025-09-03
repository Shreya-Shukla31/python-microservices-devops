from flask import Flask, request, jsonify
import os
app = Flask(__name__)
LOG_PATH = "/app/logs/events.log"

@app.route("/log", methods=["POST"])
def log_event():
    data = request.json or {}
    with open(LOG_PATH, "a") as f:
        f.write(f"{data}\n")
    return jsonify({"status":"ok"}), 200