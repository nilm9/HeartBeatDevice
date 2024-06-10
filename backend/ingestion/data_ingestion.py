import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import datetime
import os
import warnings
warnings.filterwarnings("ignore", message="NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+")

# Set up InfluxDB client
token = 'mTiidoiHw2X7h5sOlVwyUeMTdXGeFedLfseFlBmqTEAVJcoa5yk3ZGwgN_gSTLMLhOfxJOz5E_ADXkulhsEouw'
org = "None"
bucket = "sleep_tracker"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    timestamp, heart_rate = map(int, msg.payload.decode().split(','))
    point = {
        "measurement": "heart_rate",
        "tags": {"user_id": "user1"},
        "time": datetime.datetime.fromtimestamp(timestamp).isoformat(),
        "fields": {"value": heart_rate}
    }
    write_api.write(bucket=bucket, org=org, record=point)

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Use localhost as the MQTT broker address
mqtt_broker_address = "localhost"

mqtt_client.connect(mqtt_broker_address, 1883, 60)
mqtt_client.subscribe("sleep_tracker/heart_rate")

mqtt_client.loop_forever()