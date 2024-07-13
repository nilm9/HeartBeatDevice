import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.thingspeak import read_from_thingspeak
from backend.kafka.real_time_processing import PreprocessFunction  # Assuming you have real-time processing setup

heartbeat_bp = Blueprint('heartbeat', __name__)

# Real-time preprocessor instance
preprocessor = PreprocessFunction()

@heartbeat_bp.route('/heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.json
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    heart_rate = data['heart_rate']

    # Prepare data for real-time processing
    new_data = pd.DataFrame([{'timestamp': timestamp, 'heart_rate': heart_rate}])
    processed_data = preprocessor.update(new_data)

    # Example of how to use processed data
    for _, row in processed_data.iterrows():
        print(f"Processed data: {row}")

    return jsonify({"status": "success"}), 200

@heartbeat_bp.route('/read_heartbeats', methods=['GET'])
def read_heartbeats():
    data = read_from_thingspeak()
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Failed to read data from ThingSpeak"}), 500
