# open unique_artists.json file and get the id of each artist and get all the albums of each artist and than all the tracks from all the albums

import base64
import json
import requests


client_id = "f30935dbf75343dfa95d0910742027ad"
client_secret = "7ec5594edbcf4d0ba40353bd2b97d8dc"
# Load the JSON file
# get the code from the URL
code = "AQCSCOxY01_EKVurSgnCgFS2gwaioIByCX0e602dyvjhgZa1xwr9EoV-EOfFn1Mq_kOBoavok0PrxbAxf9Qz1khRpWALwVg7NZrgP-T1kNtPEHYt6odu-DbThtHVen6eY9LsistLCQjulz0HD0vZu6zVMayjQxvSwHJke34amTM7JdAs65pi-TREHSEB_VGnzpzNexw"

encoded_credentials = base64.b64encode(
    client_id.encode() + b":" + client_secret.encode()
).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded",
}

token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:7777/callback",
}

r = requests.post(
    "https://accounts.spotify.com/api/token", data=token_data, headers=token_headers
)

token = r.json()["access_token"]

# Get the access token

with open("unique_artists.json", "r") as file:
    all_artists = json.load(file)

# Get all the albums of each unique_artists
albums = []
for artist in all_artists:
    artist_id = artist["id"]
    print(artist_id)
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            for album in data["items"]:
                album_info = {
                    "id": album["id"],
                    "name": album["name"],
                    "type": album["type"],
                    "release_date": album["release_date"],
                }
                print(album_info)
                albums.append(album_info)

# Get all the tracks from all the albums
tracks = []
for album in albums:
    album_id = album["id"]
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            for track in data["items"]:
                track_info = {
                    "id": track["id"],
                    "name": track["name"],
                    "type": track["type"],
                    "duration_ms": track["duration_ms"],
                }
                tracks.append(track_info)

# Write the tracks to a new JSON file
with open("all_tracks.json", "w") as file:
    json.dump(tracks, file, indent=4)
# The snippet first loads the unique_artists.json file and then gets all the albums of each artist. The albums are then used to get all the tracks from each album. Finally, the tracks are written to a new JSON file called all_tracks.json.
#
# Note: The token variable is assumed to be defined and contains the access token for the Spotify API. The token should be obtained using the appropriate authentication flow for the Spotify API.
#
# The snippet uses the requests library to make HTTP requests to the Spotify API. The response from the API is then processed to extract the required data (albums and tracks) and store it in a JSON file.

