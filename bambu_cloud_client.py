import requests
import json
import os
from pathlib import Path

# Constants
API_BASE_URL = "https://api.bambulab.com/v1" # As per research
# Based on bambulab-authentication-cli, the login endpoint is more specific
# and might involve multiple steps or a different path for direct username/password login
# For now, using a placeholder and assuming a direct login, this will need verification.
# The ondrovic/bambulab-authentication-cli uses 'https://bambulab.com/api/sign-in/tfa' for MFA step.
# The initial username/password auth endpoint used by that CLI (before MFA) appears to be this one,
# based on community understanding and its .env.example which sets BAMBU_API_URL for this base.
AUTH_ENDPOINT = API_BASE_URL + "/user/login" # Confirmed as the initial auth endpoint by ondrovic/bambulab-authentication-cli structure
PRINTERS_ENDPOINT = API_BASE_URL + "/user/device" # UPDATED GUESS: Based on some community discussions, /user/device or /device might be used. Still speculative.

USER_AGENT = "Printago Manager/0.1" # Placeholder, ideally mimic official clients
# From bambulab-authentication-cli .env.example:
# BAMBU_USER_AGENT=bambu_network_agent/01.09.05.01
# BAMBU_CLIENT_NAME=OrcaSlicer
# BAMBU_CLIENT_TYPE=slicer
# BAMBU_CLIENT_VERSION=01.09.05.51
# For simplicity, we'll use a basic user agent first.
# More specific headers might be needed for the actual API.
CLIENT_METADATA_HEADERS = {
    "User-Agent": USER_AGENT,
    # "Bambu_Client_Name": "OrcaSlicer", # Example if mimicking
    # "Bambu_Client_Type": "slicer",   # Example if mimicking
    # "Bambu_Client_Version": "01.09.05.51" # Example if mimicking
}

# Token storage configuration
APP_DATA_DIR_NAME = ".printago_manager" # Consider renaming if app name changes
TOKEN_FILE_NAME = "cloud_auth.json"

def get_token_storage_path():
    """Gets the platform-agnostic path for storing the token file."""
    home = Path.home()
    app_data_dir = home / APP_DATA_DIR_NAME
    app_data_dir.mkdir(parents=True, exist_ok=True) # Ensure directory exists
    return app_data_dir / TOKEN_FILE_NAME

def authenticate(email, password): # Renamed username to email
    """
    Authenticates the user with the Bambu Lab cloud API.
    NOTE: This is a simplified placeholder. Real Bambu Lab authentication
    might involve multiple steps, different endpoints, or specific payload structures
    as seen in tools like bambulab-authentication-cli.
    This function likely needs significant refinement based on actual API behavior.
    The payload key 'username' is used as per research on how Bambu Lab API handles email-formatted usernames.
    """
    payload = {
        "username": email, # Changed key from "account" to "username" and using the email parameter
        "password": password
        # 'client_id': '...', # Official clients might use a client_id
        # 'grant_type': 'password', # Common OAuth pattern, but Bambu might differ
    }
    headers = {**CLIENT_METADATA_HEADERS, "Content-Type": "application/json"}

    try:
        print(f"Attempting authentication to: {AUTH_ENDPOINT}")
        print(f"Payload: {json.dumps(payload)}") # Be careful logging passwords in real apps
        print(f"Headers: {headers}")
        
        response = requests.post(AUTH_ENDPOINT, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        print(f"Auth Response Data: {data}")

        # Placeholder: Extract token based on typical API responses.
        # The actual keys ('token', 'refresh_token', 'user_id', etc.) need to be verified against Bambu Lab's API.
        # bambulab-authentication-cli saves 'access_token', 'refresh_token', 'user_id', 'name', 'email', 'expires_at'
        access_token = data.get("token") or data.get("access_token")
        refresh_token = data.get("refresh_token")
        user_id = data.get("user_id") # Often useful
        expires_in = data.get("expires_in") # Seconds until expiry
        
        if access_token:
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": user_id,
                "expires_in": expires_in 
                # Store 'retrieved_at': time.time() if calculating expiry from 'expires_in'
            }
        else:
            print(f"Authentication failed: Token not found in response. Full response: {data}")
            return None
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error during authentication: {err}")
        print(f"Response content: {err.response.text if err.response else 'No response content'}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error during authentication: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response from authentication endpoint.")
        return None


def save_token(token_data):
    """
    Saves the token data to a local JSON file.
    TODO: Enhance security (e.g., system keychain or encryption).
    """
    token_path = get_token_storage_path()
    try:
        with open(token_path, 'w') as f:
            json.dump(token_data, f, indent=4)
        print(f"Token saved to {token_path}")
        return True
    except IOError as e:
        print(f"Error saving token: {e}")
        return False

def load_token():
    """
    Loads the token data from a local JSON file.
    TODO: Check for token expiry if 'expires_at' or 'retrieved_at' + 'expires_in' is stored.
    """
    token_path = get_token_storage_path()
    if not token_path.exists():
        return None
    
    try:
        with open(token_path, 'r') as f:
            token_data = json.load(f)
        # Basic check for access token
        if token_data and "access_token" in token_data:
            # TODO: Add expiry check here. For example:
            # if 'expires_at' in token_data and time.time() > token_data['expires_at']:
            #     print("Token expired.")
            #     # Optionally try to refresh the token here if refresh_token is available
            #     return None 
            return token_data
        return None
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading token or token file corrupted: {e}")
        return None

def get_printers(access_token):
    """
    Fetches the list of printers from the Bambu Lab cloud API.
    NOTE: This endpoint is hypothetical and needs verification.
    """
    if not access_token:
        print("No access token provided for get_printers.")
        return None

    headers = {
        **CLIENT_METADATA_HEADERS,
        "Authorization": f"Bearer {access_token}"
    }

    try:
        print(f"Fetching printers from: {PRINTERS_ENDPOINT}")
        print(f"Headers: {headers}")
        response = requests.get(PRINTERS_ENDPOINT, headers=headers, timeout=10)
        response.raise_for_status()
        
        printers_data = response.json()
        print(f"Printers API Response Data: {printers_data}")
        
        # Assuming the response is a list of printers.
        # The actual structure might be different, e.g., {'data': [...printers...]} or {'printers': [...]}.
        # This needs verification.
        if isinstance(printers_data, list):
            return printers_data
        elif isinstance(printers_data, dict) and 'data' in printers_data and isinstance(printers_data['data'], list):
            return printers_data['data'] # Common pattern
        elif isinstance(printers_data, dict) and 'printers' in printers_data and isinstance(printers_data['printers'], list):
            return printers_data['printers'] # Another common pattern
        else:
            print(f"Unexpected printer data format: {printers_data}")
            return None # Or an empty list, or raise an error
            
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error fetching printers: {err}")
        print(f"Response content: {err.response.text if err.response else 'No response content'}")
        if err.response and err.response.status_code == 401: # Unauthorized
            print("Access token might be expired or invalid.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching printers: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response from printers endpoint.")
        return None

# Example Usage (for testing this module directly)
if __name__ == '__main__':
    print("Testing Bambu Cloud Client (no actual API calls made in this example block)")
    
    # Test token storage path
    print(f"Token storage path: {get_token_storage_path()}")

    # Mock token data for testing save/load
    mock_token = {"access_token": "test_access_123", "refresh_token": "test_refresh_456", "user_id": "test_user"}
    
    if save_token(mock_token):
        loaded = load_token()
        if loaded:
            print(f"Loaded token successfully: {loaded}")
            assert loaded["access_token"] == "test_access_123"
        else:
            print("Failed to load token.")
    else:
        print("Failed to save token.")

    # To test authenticate() and get_printers(), you would need valid credentials
    # and to run this script in an environment where it can make network requests.
    # Example (requires valid credentials and actual API functionality):
    # username = "YOUR_BAMBU_EMAIL"
    # password = "YOUR_BAMBU_PASSWORD"
    # auth_data = authenticate(username, password)
    # if auth_data and auth_data.get("access_token"):
    #     print("Authentication successful.")
    #     save_token(auth_data)
    #     printers = get_printers(auth_data["access_token"])
    #     if printers is not None:
    #         print(f"Found {len(printers)} printers:")
    #         for printer in printers:
    #             print(f"  - {printer.get('name', 'N/A')} (ID: {printer.get('id', 'N/A')})")
    #     else:
    #         print("Could not retrieve printers.")
    # else:
    #     print("Authentication failed.")

    # Clean up mock token file if created
    # token_file_to_clean = get_token_storage_path()
    # if token_file_to_clean.exists():
    #     try:
    #         os.remove(token_file_to_clean)
    #         print(f"Cleaned up mock token file: {token_file_to_clean}")
    #     except OSError as e:
    #         print(f"Error removing mock token file: {e}")
