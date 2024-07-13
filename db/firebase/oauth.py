import os
from dotenv import load_dotenv
import google.auth.transport.requests
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Define the required scopes
scopes = ["https://www.googleapis.com/auth/firebase.database", "https://www.googleapis.com/auth/userinfo.email"]

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

# Get OAuth2 access token
access_token = get_oauth2_access_token()
print(f"Access Token: {access_token}")
