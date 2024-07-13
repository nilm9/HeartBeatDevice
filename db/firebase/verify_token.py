import os
from dotenv import load_dotenv
import google.auth.transport.requests
from google.oauth2 import service_account
import firebase_admin
from firebase_admin import credentials
import requests

# Load environment variables from .env file
load_dotenv()

# Define the required scopes
scopes = ["https://www.googleapis.com/auth/datastore", "https://www.googleapis.com/auth/userinfo.email"]

# Authenticate a credential with the service account
def get_oauth2_access_token():
    try:
        firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS')
        if firebase_credentials_path:
            credentials = service_account.Credentials.from_service_account_file(firebase_credentials_path, scopes=scopes)
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            access_token = credentials.token
            return access_token
        else:
            raise Exception("Firebase credentials not found.")
    except Exception as e:
        raise Exception(f"Error getting OAuth2 access token: {e}")

# Initialize Firebase
def initialize_firebase():
    firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS')
    if firebase_credentials_path:
        print(f"Firebase credentials path: {firebase_credentials_path}")
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    else:
        print("Firebase credentials not found.")

initialize_firebase()

# Get OAuth2 access token
token = get_oauth2_access_token()

try:
    print("token: ", token)

    # Use the OAuth2 access token to make an authenticated request
    url = "https://firestore.googleapis.com/documents/tasks"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Token is valid")
        print("Response:", response.json())
    else:
        print("Token verification failed with status code:", response.status_code)
        print("Response:", response.text)
except Exception as e:
    print("Token verification failed:", e)
