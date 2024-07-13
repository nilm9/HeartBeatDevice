from kafka import KafkaProducer
import json
import time

# Producer configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Publish test messages
test_messages = [
    {"timestamp": 1622548800, "heart_rate": 75},
    {"timestamp": 1622548810, "heart_rate": 76},
    {"timestamp": 1622548820, "heart_rate": 77}
]

for message in test_messages:
    producer.send('sleep_tracker', value=message)
    print(f"Published: {message}")
    time.sleep(1)  # Sleep to simulate time interval between messages

producer.flush()
producer.close()
