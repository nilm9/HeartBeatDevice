#!/bin/bash

KAFKA_DIR=/usr/local/kafka  # Update this to your Kafka directory

'''
Start Zookeeper:
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties

Start Kafka Broker:
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties

List Topics:
/usr/local/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
'''

# Start Zookeeper
echo "Starting Zookeeper..."
open -a Terminal "$KAFKA_DIR/bin/zookeeper-server-start.sh $KAFKA_DIR/config/zookeeper.properties"

# Wait for Zookeeper to start
sleep 5

# Start Kafka Broker
echo "Starting Kafka Broker..."
open -a Terminal "$KAFKA_DIR/bin/kafka-server-start.sh $KAFKA_DIR/config/server.properties"

# Wait for Kafka to start
sleep 5

# Verify Kafka Broker
echo "Verifying Kafka Broker..."
"$KAFKA_DIR/bin/kafka-topics.sh" --list --bootstrap-server localhost:9092

echo "Kafka setup completed."
