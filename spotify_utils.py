import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_access_token():
    auth_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": SPOTIFY_REFRESH_TOKEN,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
    )
    return auth_response.json()["access_token"]

def make_spotify_request(method, endpoint, token, **kwargs):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/{endpoint}"
    return requests.request(method, url, headers=headers, **kwargs)