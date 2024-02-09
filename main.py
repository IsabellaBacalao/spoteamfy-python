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
code = "AQCVnqChmv73YI7Hh9VaUo5XKPw_uxJztOsc_sDGWQ1ZeYZbdxK3WiOGBBG-776DLawEaOV0ORtF9TVkFc4938Kv-h0nzQreR4JCxAusTBlLIZijUS0iBQAhlUkmadvGRO7i3tnc__2VsP0qiS3r1Ua1FjMeuBjVJLUhMX9uOKH7kYFx5eHvjxG6UmHt2r5t0oxPnzw"

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

url = "https://api.spotify.com/v1/search"
headers = {"Authorization": f"Bearer {token}"}
params = {"type": "artist", "market": "FR", "limit": 50, "offset": 150}

tab = []


for letter in alphabet:
    params["q"] = letter
    response = requests.get(url, headers=headers, params=params)

    print("Récupération des artistes commençant par la lettre :", letter)
    if response.status_code == 200:
        data = response.json()
        with open(f"./result/{letter}.json", "a") as file:
            # get id, popularity, type, genres from data
            for artist in data["artists"]["items"]:
                currentID = artist["id"]
                currentPopularity = artist["popularity"]
                currentType = artist["type"]
                currentGenres = artist["genres"]
                artist = {
                    "id": currentID,
                    "popularity": currentPopularity,
                    "type": currentType,
                    "genres": currentGenres,
                }

                tab.append(artist)
            print(tab)
            file.write(json.dumps(tab))
            tab = []

    else:
        print("Erreur:", response.text)


bigFile = open("./result/artists.json", "a")
