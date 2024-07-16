import json
import logging
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
import os
from backend.thingspeak import read_from_thingspeak

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def main():
    user_id = "user123"  # Example user ID to include in the data
    while True:
        try:
            data = read_from_thingspeak()
            if data:
                for record in data:
                    record['user_id'] = user_id  # Add user_id to each record
                    producer.send('sleep_tracker', value=record)
                    print(f"Sent: {record}")
                time.sleep(60)  # Sleep to simulate data fetch interval
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Sleep before retrying in case of error

if __name__ == "__main__":
    main()
