from influxdb_client import InfluxDBClient
import os
from dotenv import load_dotenv

load_dotenv()

def setup_influxdb():
    token = os.getenv('INFLUXDB_TOKEN')
    org = os.getenv('INFLUXDB_ORG')
    url = os.getenv('INFLUXDB_URL')
    bucket_name = os.getenv('INFLUXDB_BUCKET')

    client = InfluxDBClient(url=url, token=token, org=org)
    buckets_api = client.buckets_api()

    buckets = buckets_api.find_buckets().buckets
    if not any(bucket.name == bucket_name for bucket in buckets):
        buckets_api.create_bucket(bucket_name=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

    client.close()

if __name__ == '__main__':
    setup_influxdb()
