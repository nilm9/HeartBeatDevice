import os

from kafka import KafkaConsumer
import json

# Ensure sensitive configurations are loaded from environment variables
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Consumer configuration
consumer = KafkaConsumer(
    'sleep_tracker',
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='test-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Consumed: {message.value}")
