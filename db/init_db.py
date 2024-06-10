from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient('mongodb+srv://nilmonfort98:gKtf57baArz54CoX@cluster0.wjsrhed.mongodb.net/')
db = client.sleep_tracker

# Load schemas
with open('schema/heart_rate_schema.json') as f:
    heart_rate_schema = json.load(f)

with open('schema/user_schema.json') as f:
    user_schema = json.load(f)

# Create collections with schema validation
db.create_collection("heart_rate_data", validator={"$jsonSchema": heart_rate_schema})
db.create_collection("users", validator={"$jsonSchema": user_schema})

print("Collections created with schema validation.")
