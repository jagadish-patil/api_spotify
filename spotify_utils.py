import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_access_token():
    print("Client ID:", os.getenv("SPOTIFY_CLIENT_ID"))
    print("Client SECRET:", os.getenv("SPOTIFY_CLIENT_SECRET"))
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        raise Exception("Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET")

    # Build the Base64 encoded string
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=headers,
        data=data
    )

    print("Spotify auth status:", auth_response.status_code)
    print("Response:", auth_response.text)

    auth_response.raise_for_status()  # will raise error if not 2xx

    return auth_response.json()["access_token"]

def make_spotify_request(method, endpoint, token, **kwargs):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/{endpoint}"
    return requests.request(method, url, headers=headers, **kwargs)