import os
from dotenv import load_dotenv
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import logging

# Load environment variables from .env file
load_dotenv()




# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the required scopes
scopes = ["https://www.googleapis.com/auth/datastore"]

# Authenticate a credential with the service account
def get_oauth2_access_token():
    try:
        firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS')
        if firebase_credentials_path:
            logger.debug(f"Firebase credentials path: {firebase_credentials_path}")
            credentials = service_account.Credentials.from_service_account_file(
                firebase_credentials_path, scopes=scopes)
            request = Request()
            credentials.refresh(request)
            access_token = credentials.token
            logger.debug(f"Access Token: {access_token}")
            return access_token
        else:
            logger.error("Firebase credentials not found.")
    except Exception as e:
        logger.error(f"Error getting OAuth2 access token: {e}")
        raise

# Get OAuth2 access token
access_token = get_oauth2_access_token()
print(f"Access Token: {access_token}")

# Example request to Firestore using the OAuth 2.0 token
def make_authenticated_request():
    try:
        database_name = os.getenv('FIREBASE_DATABASE_NAME')
        if not database_name:
            logger.error("Database name not found in environment variables.")
            return

        # Replace <PATH> with the actual path in your Firestore database
        path = "tasks"  # Example path
        url = f"https://firestore.googleapis.com/v1/projects/{database_name}/databases/(default)/documents/{path}?access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f"Response Data: {response.json()}")
        else:
            logger.error(f"Failed to retrieve data: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Error making authenticated request: {e}")

if __name__ == "__main__":
    make_authenticated_request()
