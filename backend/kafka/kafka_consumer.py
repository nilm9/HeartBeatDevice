# kafka_consumer.py
from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import time
from dotenv import load_dotenv
import os
from backend.thingspeak import read_from_thingspeak

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Consumer configuration
consumer = KafkaConsumer(
    'sleep_tracker',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='flink-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def preprocess(data):
    timestamp = data['timestamp']
    heart_rate = data['heart_rate']

    # Calculate HRV, rolling averages, etc. (simplified example)
    hrv = heart_rate / 2  # Replace with actual HRV calculation
    rolling_mean = heart_rate  # Replace with actual rolling mean calculation
    rolling_std = heart_rate / 3  # Replace with actual rolling std calculation

    processed_data = {
        'timestamp': timestamp,
        'heart_rate': heart_rate,
        'hrv': hrv,
        'rolling_mean': rolling_mean,
        'rolling_std': rolling_std
    }

    return processed_data

# Main processing loop
def main():
    while True:
        data = read_from_thingspeak()
        if data:
            for record in data:
                processed_data = preprocess(record)
                producer.send('processed_sleep_tracker', value=processed_data)
                logger.debug(f"Processed and sent: {processed_data}")
                time.sleep(1)  # Sleep to simulate processing time

if __name__ == "__main__":
    main()
