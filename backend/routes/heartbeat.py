import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime
from influxdb import InfluxDBClient
from backend.real_time_processing import PreprocessFunction  # Assuming you have real-time processing setup

heartbeat_bp = Blueprint('heartbeat', __name__)

# Set up InfluxDB client
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('sleep_tracker')

# Real-time preprocessor instance
preprocessor = PreprocessFunction()


@heartbeat_bp.route('/heartbeat', methods=['POST'])
def receive_heartbeat():
    data = request.json
    user_id = data['user_id']
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    heart_rate = data['heart_rate']

    # Prepare data for real-time processing
    new_data = pd.DataFrame([{'timestamp': timestamp, 'heart_rate': heart_rate}])
    processed_data = preprocessor.update(new_data)

    # Example of how to use processed data
    for _, row in processed_data.iterrows():
        print(f"Processed data: {row}")

    # Store raw data in InfluxDB
    json_body = [{
        "measurement": "heart_rate",
        "tags": {
            "user_id": user_id
        },
        "time": timestamp,
        "fields": {
            "value": heart_rate
        }
    }]
    client.write_points(json_body)

    return jsonify({"status": "success"}), 200
