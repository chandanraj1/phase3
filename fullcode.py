!pip install kiteconnect gspread oauth2client --quiet
import time
import os
from kiteconnect import KiteConnect
from requests.exceptions import RequestException
from kiteconnect.exceptions import KiteException

def initialize_kite_with_retry(max_retries=5, retry_delay=15):
    for attempt in range(max_retries):
        try:
            # Retrieve API key, API secret, and access token from environment variables
            api_key = os.getenv('KITE_API_KEY')
            api_secret = os.getenv('KITE_API_SECRET')
            access_token = os.getenv('KITE_ACCESS_TOKEN')

            # Initialize KiteConnect with the API key
            kite = KiteConnect(api_key=api_key)

            # Set the access token for your session
            kite.set_access_token(access_token)

            print("Kite API initialized successfully.")
            return kite
        except (KiteException, RequestException) as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(retry_delay)  # Wait before retrying

    # After all retries have failed, raise an exception
    raise Exception("Failed to initialize Kite API after multiple retries.")

try:
    # Initialize Kite API with retry logic
    kite = initialize_kite_with_retry()

    # Example: Now you can use `kite` to make API calls, such as fetching the user profile
    profile = kite.profile()
    print(profile)

except Exception as e:
    print(f"An error occurred: {e}")
