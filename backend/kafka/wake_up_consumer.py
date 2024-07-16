import json
from kafka import KafkaConsumer
from datetime import datetime

from backend.algorithm import detect_sleep_stage
from backend.utils.notifications import send_email_notification

# Consumer configuration
consumer = KafkaConsumer(
    'processed_sleep_tracker',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='wake-up-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

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

def check_wake_up_condition(data):
    user_id = data.get('user_id')
    if not user_id:
        print("No user_id found in the data")
        return False

    preferences = user_preferences.get(user_id)
    if not preferences:
        print(f"No preferences found for user {user_id}")
        return False

    print(f"Checking wake-up condition for user {user_id} with preferences {preferences} and data {data}")

    wake_up_window_start = datetime.strptime(preferences['wake_up_window_start'], '%H:%M').time()
    wake_up_window_end = datetime.strptime(preferences['wake_up_window_end'], '%H:%M').time()
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ').time()

    print(f"Wake-up window for user {user_id}: {wake_up_window_start} to {wake_up_window_end}")
    print(f"Data timestamp: {timestamp}")

    if wake_up_window_start <= timestamp <= wake_up_window_end:
        sleep_stage = detect_sleep_stage(data['hrv'], data['rolling_mean'], data['rolling_std'])
        print(f"Detected sleep stage for user {user_id}: {sleep_stage}")
        if sleep_stage in ['wake', 'light_sleep']:
            send_wake_up_notification(user_id, data['timestamp'])
            return True
    return False

def send_wake_up_notification(user_id, timestamp):
    user_email = user_preferences[user_id]['email']
    subject = "Wake Up!"
    body = f"It's time to wake up! Optimal time: {timestamp}"
    print(f"Sending wake-up notification to {user_email} with timestamp {timestamp}")
    send_email_notification(user_email, subject, body)

# Consumer processing loop
def main():
    print("Starting wake-up logic consumer...")
    for message in consumer:
        try:
            data = message.value
            print(f"Received message: {data}")
            check_wake_up_condition(data)
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()
