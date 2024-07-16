# routes/heartbeat.py
import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.thingspeak import read_from_thingspeak

heartbeat_bp = Blueprint('heartbeat', __name__)

@heartbeat_bp.route('/heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.json
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    heart_rate = data['heart_rate']

    # Log received data
    print(f"Received heartbeat: {timestamp}, {heart_rate}")

    return jsonify({"status": "success"}), 200

@heartbeat_bp.route('/read_heartbeats', methods=['GET'])
def read_heartbeats():
    data = read_from_thingspeak()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Failed to read data from ThingSpeak"}), 500
