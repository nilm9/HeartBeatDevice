import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase
logger.debug("Initializing Firebase...")
try:
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
    firebase_admin.initialize_app(cred)
    logger.debug("Firebase initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Firebase: {e}")

# Get Firestore client
try:
    db = firestore.client()
    logger.debug("Firestore client obtained successfully.")
except Exception as e:
    logger.error(f"Failed to obtain Firestore client: {e}")

# Function to retrieve and print data from Firestore
def retrieve_data():
    try:
        user_preferences_ref = db.collection('user_preferences')
        docs = user_preferences_ref.stream()
        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
    except Exception as e:
        logger.error(f"Failed to retrieve data: {e}")

if __name__ == "__main__":
    retrieve_data()
