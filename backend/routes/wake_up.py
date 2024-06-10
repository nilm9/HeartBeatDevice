import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from pymongo import MongoClient
from backend.utils.notifications import send_email_notification
from backend.utils.preprocessing import preprocess_data
from backend.algorithm import detect_sleep_stage

wake_up_bp = Blueprint('wake_up', __name__)
user_preferences = {}

client = MongoClient('mongodb://localhost:27017/')
db = client.sleep_tracker
heart_rate_collection = db.heart_rate_data


@wake_up_bp.route('/set_wake_up_window', methods=['POST'])
def set_wake_up_window():
    data = request.json
    user_id = data['user_id']
    wake_up_window_start = datetime.strptime(data['wake_up_window_start'], '%Y-%m-%d %H:%M:%S')
    wake_up_window_end = datetime.strptime(data['wake_up_window_end'], '%Y-%m-%d %H:%M:%S')
    user_preferences[user_id] = {
        'wake_up_window_start': wake_up_window_start,
        'wake_up_window_end': wake_up_window_end
    }
    return jsonify({"status": "success"}), 200


@wake_up_bp.route('/send_wake_up_notification', methods=['POST'])
def send_wake_up_notification():
    data = request.json
    user_id = data['user_id']
    wake_up_window_start = user_preferences[user_id]['wake_up_window_start']
    wake_up_window_end = user_preferences[user_id]['wake_up_window_end']

    # Retrieve heart rate data within the wake-up window
    heart_rate_data = list(heart_rate_collection.find({
        'user_id': user_id,
        'timestamp': {'$gte': wake_up_window_start, '$lte': wake_up_window_end}
    }))
    heart_rate_data = pd.DataFrame(heart_rate_data)

    # Preprocess the data
    preprocessed_data = preprocess_data(heart_rate_data)

    # Find the optimal wake-up time
    optimal_wake_up_time = None
    for _, row in preprocessed_data.iterrows():
        sleep_stage = detect_sleep_stage(row['normalized_hrv'], row['normalized_rolling_mean'],
                                         row['normalized_rolling_std'])
        if sleep_stage in ['wake', 'light_sleep']:
            optimal_wake_up_time = row['timestamp']
            break

    if not optimal_wake_up_time:
        optimal_wake_up_time = wake_up_window_end  # Default to the end of the window

    # Send email notification
    user_email = "user_email@example.com"  # Retrieve from user profile
    subject = "Wake Up!"
    body = f"It's time to wake up! Optimal time: {optimal_wake_up_time}"
    send_email_notification(user_email, subject, body)

    return jsonify({"status": "notification sent", "optimal_wake_up_time": optimal_wake_up_time}), 200
