import json
import logging
import requests
import base64
import sys

logging.basicConfig(level=logging.INFO)


def getNewToken(client_id, client_secret):
    encoded_credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {"grant_type": "client_credentials"}
    token_headers = {"Authorization": f"Basic {encoded_credentials}"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token = token_response.json()["access_token"]
    return token


def get_track_data(track_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://api.spotify.com/v1/audio-analysis/{track_id}", headers=headers
    )
    return response.json()


def get_audio_features(track_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://api.spotify.com/v1/audio-features/{track_id}", headers=headers
    )
    return response.json()


def main(starting_track_id=None):
    client_id = "f30935dbf75343dfa95d0910742027ad"
    client_secret = "7ec5594edbcf4d0ba40353bd2b97d8dc"

    token = getNewToken(client_id, client_secret)

    with open("all_tracks.json") as f:
        track_ids = json.load(f)

    if starting_track_id:
        try:
            index = track_ids.index(starting_track_id)
            track_ids = track_ids[index:]
        except ValueError:
            logging.error(
                f"Starting track ID '{starting_track_id}' not found in the list."
            )
            sys.exit(1)

    all_tracks_data = []

    for track_id in track_ids:
        try:
            logging.info(f"Processing track ID: {track_id}")
            track_data = get_track_data(track_id, token)
            audio_features = get_audio_features(track_id, token)

            combined_data = {
                "track_id": track_id,
                "analysis_data": track_data,
                "features_data": audio_features,
            }
            all_tracks_data.append(combined_data)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logging.error("Rate limit exceeded. Exiting...")
                with open("error_data.json", "w") as error_file:
                    json.dump(all_tracks_data, error_file, indent=4)
                sys.exit(1)
            else:
                logging.error(f"HTTP Error occurred for track ID {track_id}: {e}")
                with open("error_data.json", "w") as error_file:
                    json.dump(all_tracks_data, error_file, indent=4)
                sys.exit(1)
        except Exception as e:
            logging.error(f"Error processing track ID {track_id}: {e}")
            with open("error_data.json", "w") as error_file:
                json.dump(all_tracks_data, error_file, indent=4)
            sys.exit(1)

    with open("all_tracks_data.json", "w") as f:
        json.dump(all_tracks_data, f, indent=4)

    logging.info("All tracks processed successfully.")


if __name__ == "__main__":
    starting_track_id = input(
        "Enter the starting track ID (or leave blank to start from the beginning): "
    ).strip()
    if starting_track_id:
        main(starting_track_id)
    else:
        main()
