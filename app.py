import os

from flask import Flask, jsonify, request
from spotify_utils import get_access_token, make_spotify_request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

port = int(os.environ.get("PORT", 5000))  # fallback for local dev

@app.route("/spotify/top-tracks", methods=["GET"])
def top_tracks():
    token = get_access_token()
    res = make_spotify_request("GET", "me/top/tracks?limit=10", token)
    data = res.json()
    return jsonify([
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "id": t["id"],
            "uri": t["uri"]
        } for t in data["items"]
    ])

@app.route("/spotify/now-playing", methods=["GET"])
def now_playing():
    token = get_access_token()
    res = make_spotify_request("GET", "me/player/currently-playing", token)
    if res.status_code == 204:
        return jsonify({"message": "Nothing is playing"})
    data = res.json()
    return jsonify({
        "name": data["item"]["name"],
        "artist": data["item"]["artists"][0]["name"]
    })

@app.route("/spotify/play", methods=["POST"])
def play_song():
    token = get_access_token()
    track_uri = request.json.get("uri")
    if not track_uri:
        return jsonify({"error": "Track URI required"}), 400

    res = make_spotify_request(
        "PUT", "me/player/play", token,
        json={"uris": [track_uri]}
    )
    return jsonify({"status": "playing", "track_uri": track_uri})

@app.route("/spotify/pause", methods=["POST"])
def pause_song():
    token = get_access_token()
    res = make_spotify_request("PUT", "me/player/pause", token)
    return jsonify({"status": "paused"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)