import os
import requests
from dotenv import load_dotenv
import logging
from db.firebase.bearer_token import get_oauth2_access_token

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Function to test the endpoint
def test_set_wake_up_window():
    # Get the access token from the environment variables or fetch it using your script
    access_token = get_oauth2_access_token()

    if not access_token:
        logger.error("Access token could not be obtained.")
        return

    logger.debug(f"Access Token: {access_token}")

    # Define the API endpoint
    url = "http://localhost:5000/set_wake_up_window"

    # Define the payload
    payload = {
        "wake_up_window_start": "07:00",
        "wake_up_window_end": "08:00"
    }

    # Define the headers, including the bearer token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Print the response status code
    logger.debug(f"Status Code: {response.status_code}")

    # Print the raw response content
    logger.debug(f"Response Content: {response.content}")

    # Try to parse the JSON response
    try:
        response_json = response.json()
        logger.debug(f"Response JSON: {response_json}")
    except ValueError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        response_json = {}

    # Assertions to validate the response
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.content.decode('utf-8')}"
    assert response_json.get("status") == "success"


if __name__ == "__main__":
    test_set_wake_up_window()
