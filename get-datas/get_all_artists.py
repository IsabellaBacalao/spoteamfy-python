import requests
from urllib.parse import urlencode
import base64
import webbrowser
import json

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


# get the code from the URL
code = "AQBqhlGooPjSauYVcI4p5YuLPYhtAoHoKFmbK306LEA1bC33CHEndPgLUdXz5FqZEM0j6NF_0Namwm_uqDqufGNQLoVnDVNTnyhfVtcSAW-nbeNisiqiOhwvcDqKBkrbUnoFRnkpuUzS0Is-CjYFyo2xLGIW1V88YEScdy4NRbGBupGaSYywwEIcZpiAvzZb6YFhYQA"

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


user_headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

user_params = {"limit": 50}

alphabet = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

# alphabet = [chr(i) for i in range(97, 123)]  # Generating lowercase alphabet
search_type = "artist"
market = "FR"
limit = 50

all_artists = []

for letter in alphabet:
    for offset in range(0, 200, limit):  # Assuming maximum of 200 artists per letter
        url = f"https://api.spotify.com/v1/search?q={letter}&type={search_type}&market={market}&limit={limit}&offset={offset}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "artists" in data:
                artists = data["artists"]["items"]
                for artist in artists:
                    artist_info = {
                        "id": artist["id"],
                        "name": artist["name"],
                        "type": artist["type"],
                        "genres": artist["genres"],
                    }
                    all_artists.append(artist_info)

# Writing all_artists to a JSON file
with open("all_artists.json", "w") as outfile:
    json.dump(all_artists, outfile, indent=4)

print("Data written to all_artists.json")
