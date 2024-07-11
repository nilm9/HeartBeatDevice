from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.sleep_tracker

with open('schema/heart_rate_schema.json') as f:
    heart_rate_schema = json.load(f)

with open('schema/user_schema.json') as f:
    user_schema = json.load(f)

db.create_collection("heart_rate_data", validator={"$jsonSchema": heart_rate_schema})
db.create_collection("users", validator={"$jsonSchema": user_schema})

print("Collections created with schema validation.")
