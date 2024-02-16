import requests
import time
import base64
import json
import random

counter = 1


def getNextSecret():
    global counter
    if counter == 1:
        client_id = "1cba597e55d94b3d87ee781a30363ed7"
        client_secret = "f8a0dd1992e743668702625e61906739"
    elif counter == 2:
        client_id = "f30935dbf75343dfa95d0910742027ad"
        client_secret = "7ec5594edbcf4d0ba40353bd2b97d8dc"
    else:
        client_id = "9707531cd3a04695935120e738853d73"
        client_secret = "f1f9175956d844048ac9a781d3e72f05"
    counter = (counter % 3) + 1
    return client_id, client_secret


def getNewToken():
    client_id, client_secret = getNextSecret()
    encoded_credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {encoded_credentials}"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token = token_response.json()["access_token"]
    return token


# Function to fetch tracks of an album
def get_album_tracks(album_id):
    tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    tracks_headers = {"Authorization": f"Bearer {getNewToken()}"}
    tracks_response = requests.get(tracks_url, headers=tracks_headers)
    # numberOfTracks = tracks_response.json()["total"]
    # print(f"Number of tracks : {numberOfTracks}")
    if tracks_response.status_code == 200:
        # return tracks_response.json()["items"]
        tracks_data = tracks_response.json()["items"]
        return [track["id"] for track in tracks_data]
    else:
        return None


# Function to fetch albums of an artist
def get_artist_albums(artist_id):
    try:
        albums_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        albums_headers = {"Authorization": f"Bearer {getNewToken()}"}
        albums_response = requests.get(albums_url, headers=albums_headers)

        if albums_response.status_code == 200:
            albums_data = albums_response.json()
            total_albums = albums_data.get("total", 0)
            print(f"Total albums found for artist ID {artist_id}: {total_albums}")

            if total_albums > 0:
                albums = albums_data.get("items", [])
                album_ids = [album["id"] for album in albums]
                return album_ids
            else:
                print(f"No albums found for artist ID: {artist_id}")
                return []
        else:
            print(f"Failed to fetch albums for artist ID: {artist_id}")
            print(f"Status code: {albums_response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching albums for artist ID: {artist_id}")
        print(f"Error details: {e}")
        return None
    except Exception as e:
        print(
            f"An unexpected error occurred while fetching albums for artist ID: {artist_id}"
        )
        print(f"Error details: {e}")
        return None


# Retrieving artist data from JSON
with open("all_artists.json", "r") as artist_file:
    all_artists = json.load(artist_file)

# Retrieving tracks of all albums of all artists
all_tracks = []
for artist in all_artists:
    print(f"Fetching tracks for", artist["name"], "(" + artist["id"] + ")")
    artist_albums = get_artist_albums(artist["id"])
    if artist_albums:
        for album_id in artist_albums:
            print("Fetching tracks for album", album_id)
            album_tracks = get_album_tracks(album_id)
            if album_tracks:
                all_tracks.extend(album_tracks)
                with open("all_tracks.json", "r") as outfile:
                    file = json.load(outfile)
                    file.extend(album_tracks)
                with open("all_tracks.json", "w") as outfile:
                    json.dump(file, outfile, indent=4)
                    time.sleep(0.3)


# Writing all tracks to a JSON file
# with open("all_tracks.json", "w") as outfile:
#     json.dump(all_tracks, outfile, indent=4)
#
print("Data written to all_tracks.json")
