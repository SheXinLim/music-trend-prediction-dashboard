import requests
import base64
import json
import os
import pandas as pd
from dotenv import load_dotenv  # Load API keys securely

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    token_info = response.json()
    return token_info["access_token"]

# Function to get trending artists dynamically from Spotify charts
def get_top_artists(token, limit=10):
    url = f"https://api.spotify.com/v1/browse/new-releases?limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    albums = response.json().get("albums", {}).get("items", [])
    
    artists = []
    for album in albums:
        for artist in album["artists"]:
            artists.append(artist["name"])
    return list(set(artists))  # Remove duplicates

# Function to search for an artist
def search_artist(artist_name, token):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    artist_data = response.json()
    
    if artist_data["artists"]["items"]:
        return artist_data["artists"]["items"][0]
    return None

# Function to get top tracks for an artist
def get_artist_top_tracks(artist_id, token, market="US"):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return response.json()["tracks"]

# Function to get audio features of a track
def get_audio_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    return response.json()

# Authenticate and get token
token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)

# Get trending artists dynamically
artist_names = get_top_artists(token, limit=15)

# Data collection
spotify_data = []

for artist_name in artist_names:
    artist_info = search_artist(artist_name, token)
    
    if artist_info:
        artist_id = artist_info["id"]
        artist_popularity = artist_info["popularity"]
        artist_followers = artist_info["followers"]["total"]
        genres = ", ".join(artist_info["genres"])

        top_tracks = get_artist_top_tracks(artist_id, token)
        
        for track in top_tracks:
            # Get audio features for deeper insights
            audio_features = get_audio_features(track["id"], token)
            
            spotify_data.append({
                "artist": artist_name,
                "artist_id": artist_id,
                "artist_popularity": artist_popularity,
                "artist_followers": artist_followers,
                "genres": genres,
                "track_name": track["name"],
                "track_id": track["id"],
                "track_popularity": track["popularity"],
                "release_date": track["album"]["release_date"],
                "danceability": audio_features.get("danceability"),
                "energy": audio_features.get("energy"),
                "tempo": audio_features.get("tempo"),
            })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(spotify_data)
df.to_csv("spotify_trending_artists.csv", index=False)

print("✅ Data saved to spotify_trending_artists.csv")
