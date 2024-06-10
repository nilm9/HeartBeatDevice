import paho.mqtt.client as mqtt
import time

def publish_test_data(broker_address="localhost", topic="sleep_tracker/heart_rate"):
    # Set up MQTT client
    mqtt_client = mqtt.Client()

    # Connect to the MQTT broker
    mqtt_client.connect(broker_address, 1883, 60)

    # Publish test messages
    test_messages = [
        "1622548800,75",
        "1622548810,76",
        "1622548820,77",
        "1622548830,78",
        "1622548840,79"
    ]

    for message in test_messages:
        mqtt_client.publish(topic, message)
        print(f"Published: {message}")
        time.sleep(1)  # Sleep to simulate time interval between messages

    mqtt_client.disconnect()
    print("Disconnected from MQTT broker")

if __name__ == "__main__":
    publish_test_data()
