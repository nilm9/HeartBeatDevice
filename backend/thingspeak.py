# thingspeak_utils.py
import os
import requests
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

THINGSPEAK_API_KEY = os.getenv('THINGSPEAK_API_KEY')
THINGSPEAK_READ_URL = os.getenv('THINGSPEAK_READ_URL')

def read_from_thingspeak(results=100):
    url = f"{THINGSPEAK_READ_URL}?api_key={THINGSPEAK_API_KEY}&results={results}"
    logger.debug(f"Request URL: {url}")
    response = requests.get(url)
    logger.debug(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json().get('feeds', [])
        logger.debug(f"Data retrieved: {data}")
        return data
    else:
        logger.error(f"Failed to read data from ThingSpeak: {response.status_code}")
        logger.error(f"Response Text: {response.text}")
        return None

# Test the function
if __name__ == "__main__":
    data = read_from_thingspeak()
    if data:
        logger.info("Successfully read data from ThingSpeak.")
        import pandas as pd
        print(pd.DataFrame(data))
    else:
        logger.error("Failed to read data from ThingSpeak.")
