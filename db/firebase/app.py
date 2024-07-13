import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Setup logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Firebase
def initialize_firebase():
    firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS')
    if firebase_credentials_path:
        logger.debug(f"Firebase credentials path: {firebase_credentials_path}")
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
        logger.debug("Firebase initialized successfully.")
    else:
        logger.error("Firebase credentials not found.")

# Get Firestore client
def get_firestore_client():
    try:
        client = firestore.client()
        logger.debug("Firestore client obtained successfully.")
        return client
    except Exception as e:
        logger.error(f"Error getting Firestore client: {e}")
        raise

initialize_firebase()
db = get_firestore_client()

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None

@app.route('/verify_token', methods=['POST'])
def verify_token_endpoint():
    token = request.json.get('token')
    user_id = verify_token(token)
    if user_id:
        return jsonify({"uid": user_id, "message": "Token is valid"}), 200
    else:
        return jsonify({"error": "Invalid or expired token"}), 401

@app.route('/set_wake_up_window', methods=['POST'])
def set_wake_up_window():
    data = request.json
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        id_token = auth_header.split(' ')[1]
        user_id = verify_token(id_token)
        if user_id:
            logger.debug(f"Received data: {data}")
            wake_up_window_start = data['wake_up_window_start']
            wake_up_window_end = data['wake_up_window_end']
            try:
                db.collection('user_preferences').document(user_id).set({
                    'wake_up_window_start': wake_up_window_start,
                    'wake_up_window_end': wake_up_window_end
                })
                logger.debug(f"Data for user {user_id} stored successfully.")
                return jsonify({"status": "success"}), 200
            except Exception as e:
                logger.error(f"Error: {e}")
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Invalid ID token"}), 401
    else:
        return jsonify({"error": "Authorization header missing or invalid"}), 401

if __name__ == "__main__":
    app.run(debug=True)
