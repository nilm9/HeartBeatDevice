# routes/wake_up.py
import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.utils.notifications import send_email_notification
from backend.algorithm import detect_sleep_stage

wake_up_bp = Blueprint('wake_up', __name__)

user_preferences = {
    "user123": {
        "wake_up_window_start": "07:00",
        "wake_up_window_end": "08:00",
        "email": "user123@example.com",
        "preferences": {
            "notification": "email",
            "timezone": "UTC"
        }
    }
}

@wake_up_bp.route('/set_wake_up_window', methods=['POST'])
def set_wake_up_window():
    data = request.json
    user_id = data['user_id']
    wake_up_window_start = data['wake_up_window_start']
    wake_up_window_end = data['wake_up_window_end']
    user_preferences[user_id] = {
        'wake_up_window_start': wake_up_window_start,
        'wake_up_window_end': wake_up_window_end,
        'email': data['email'],
        'preferences': data['preferences']
    }
    return jsonify({"status": "success"}), 200
