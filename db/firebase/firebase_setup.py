import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv()


# Initialize Firebase
def initialize_firebase():
    cred_path = os.getenv("FIREBASE_CREDENTIALS")
    if not cred_path:
        raise ValueError("FIREBASE_CREDENTIALS environment variable not set.")

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


# Get Firestore client
def get_firestore_client():
    return firestore.client()


if __name__ == "__main__":
    initialize_firebase()
    db = get_firestore_client()
    print("Firebase initialized and Firestore client obtained.")
