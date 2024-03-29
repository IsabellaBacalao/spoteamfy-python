import requests
import time
import base64
import json
import random

# client_id = "f30935dbf75343dfa95d0910742027ad"
# client_secret = "41273d9784e44293b467b88d66bcd45e"
client_id = "f30935dbf75343dfa95d0910742027ad"
client_secret = "7ec5594edbcf4d0ba40353bd2b97d8dc"

canGo = False


def getNewToken():
    encoded_credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {encoded_credentials}"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token = token_response.json()["access_token"]
    return token


token = getNewToken()


# Function to fetch tracks of an album
def get_album_tracks(album_id):
    tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    tracks_headers = {"Authorization": f"Bearer {token}"}
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
        albums_headers = {"Authorization": f"Bearer {token}"}
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


id_recherche = "6ZjFtWeHP9XN7FeKSUe80S"  # ID of the artist to search for
# Retrieving artist data from JSON
with open("all_artists.json", "r") as artist_file:
    all_artists = json.load(artist_file)
    index_id_recherche = next(
        (index for (index, d) in enumerate(all_artists) if d["id"] == id_recherche),
        None,
    )
    if index_id_recherche is not None:
        filtered_artists = all_artists[index_id_recherche:]
    else:
        filtered_artists = all_artists

# Retrieving tracks of all albums of all artists
all_tracks = []
print("Total artists:", len(all_artists))
print("Total remaining artists to fetch tracks for:", len(filtered_artists))
print("filtered_artists:", filtered_artists[0])

for artist in filtered_artists:
    if artist["id"] == "1q7T9rFQ2a2ukA1PU51fo3":  # kobalad
        canGo = True

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
                        # time.sleep(0.3)

    if canGo == False:
        print(f"Skipping", artist["name"], "(" + artist["id"] + ")")
        continue


# Writing all tracks to a JSON file
# with open("all_tracks.json", "w") as outfile:
#     json.dump(all_tracks, outfile, indent=4)
#
print("Data written to all_tracks.json")
