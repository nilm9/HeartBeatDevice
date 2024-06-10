from influxdb_client import InfluxDBClient
import os

# brew services stop influxdb
def setup_influxdb():
    # Token should be securely stored, here we use an environment variable for demonstration
    token = 'mTiidoiHw2X7h5sOlVwyUeMTdXGeFedLfseFlBmqTEAVJcoa5yk3ZGwgN_gSTLMLhOfxJOz5E_ADXkulhsEouw=='
    org = "None"  # Replace with your organization name
    url = "http://localhost:8086"

    client = InfluxDBClient(url=url, token=token, org=org)
    buckets_api = client.buckets_api()

    bucket_name = "sleep_tracker"
    buckets = buckets_api.find_buckets().buckets
    if not any(bucket.name == bucket_name for bucket in buckets):
        buckets_api.create_bucket(bucket_name=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

    client.close()

if __name__ == '__main__':
    setup_influxdb()
