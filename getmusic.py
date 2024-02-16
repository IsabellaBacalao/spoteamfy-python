import base64
import json
import requests
import logging
import webbrowser
from urllib.parse import urlencode

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

client_id = "f30935dbf75343dfa95d0910742027ad"
client_secret = "7ec5594edbcf4d0ba40353bd2b97d8dc"

auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read",
}

auth_url = "https://accounts.spotify.com/authorize?" + urlencode(auth_headers)
# webbrowser.open(auth_url)

code = "AQCgmj9B0sSjpaFxK8rt1C1MVa3Rs5vZOOfVAD8TDn7TKHzO20I7lOumhJMuhrBaZwuoTWuNJUzHM1FYRcREoZIfABk7a2fU3z45LYn3kuKSXYAzd53EpejVhSyTz78Q7v94M_aOrTIbXJaR2Z5VOawTuKdjwXHKuyv0IBBPgqo30VbPgPFx4c3I3cQc_qchqWiF4oA"


def get_spotify_token(client_id, client_secret, code):
    """
    Authenticate with the Spotify API and get an access token.
    """
    logging.info("Starting authentication process to get access token.")
    encoded_credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:7777/callback",
    }
    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        response.raise_for_status()  # Raises an HTTPError if the response is not 2xx
        access_token = response.json()["access_token"]
        logging.info("Successfully obtained access token.")
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to authenticate and obtain access token: {e}")
        return None


def fetch_albums_for_artist(access_token, artist_id):
    """
    Fetch all albums for a given artist using Spotify API, handling pagination.
    """
    logging.info(f"Fetching albums for artist ID: {artist_id}")
    albums = []
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50"  # Max limit
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response is not 2xx
            data = response.json()
            albums.extend(data["items"])
            url = data.get("next")  # Move to next page if exists
            logging.info(f"Fetched {len(data['items'])} albums. Moving to next page.")
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            retry_after = int(response.headers["Retry-After"])
            logging.warning(f"Rate limited. Retrying after {retry_after} seconds.")
            # time.sleep(retry_after)
            # return fetch_albums_for_artist(access_token, artist_id)
        logging.error(f"Error fetching albums: {e}")
    return albums


def fetch_tracks_for_album(access_token, album_id):
    """
    Fetch all tracks from a given album using Spotify API, handling pagination.
    """
    logging.info(f"Fetching tracks for album ID: {album_id}")
    tracks = []
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50"  # Max limit
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the response is not 2xx
            data = response.json()
            tracks.extend(data["items"])
            url = data.get("next")  # Move to next page if exists
            logging.info(f"Fetched {len(data['items'])} tracks. Moving to next page.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching tracks: {e}")
    return tracks


def main():
    """
    Main function to orchestrate the fetching process.
    """
    # Example placeholder values; replace with actual credentials and code
    # client_id = "your_client_id"
    # client_secret = "your_client_secret"
    # code = "your_authorization_code"

    token = get_spotify_token(client_id, client_secret, code)
    if token:
        try:
            with open("unique_artists.json", "r") as file:
                all_artists = json.load(file)
                logging.info(f"Loaded {len(all_artists)} artists.")

            all_tracks = []
            for artist in all_artists:
                albums = fetch_albums_for_artist(token, artist["id"])
                for album in albums:
                    tracks = fetch_tracks_for_album(token, album["id"])
                    all_tracks.extend(tracks)

            with open("all_tracks.json", "w") as file:
                json.dump(all_tracks, file, indent=4)
                logging.info(
                    f"Successfully saved {len(all_tracks)} tracks to all_tracks.json."
                )
        except Exception as e:
            logging.error(f"An error occurred during the fetching process: {e}")
    else:
        logging.error("Failed to obtain access token. Cannot proceed.")


if __name__ == "__main__":
    main()
