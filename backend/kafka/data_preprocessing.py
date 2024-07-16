import json
import time
from kafka import KafkaConsumer, KafkaProducer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Consumer configuration
consumer = KafkaConsumer(
    'sleep_tracker',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='preprocess-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def preprocess(data):
    timestamp = data['created_at']
    heart_rate = float(data['field2'])

    hrv = heart_rate / 2
    rolling_mean = heart_rate
    rolling_std = heart_rate / 3

    processed_data = {
        'timestamp': timestamp,
        'heart_rate': heart_rate,
        'hrv': hrv,
        'rolling_mean': rolling_mean,
        'rolling_std': rolling_std,
        'user_id': data['user_id']  # Ensure user_id is included in processed data
    }

    return processed_data

# Main processing loop
def main():
    for message in consumer:
        data = message.value
        print(f"Data received from Kafka: {data}")

        preprocessed_data = preprocess(data)
        if preprocessed_data:
            try:
                producer.send('processed_sleep_tracker', value=preprocessed_data)
                print(f"Preprocessed data sent to Kafka: {preprocessed_data}")
            except Exception as e:
                print(f"Error sending preprocessed data to Kafka: {e}")
        time.sleep(1)  # Simulate processing delay

if __name__ == "__main__":
    main()
