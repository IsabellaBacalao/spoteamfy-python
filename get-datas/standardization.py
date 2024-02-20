# import all_artists.json file and standardize the data (remove duplicates, etc.))

import json
import os

# Load the JSON file
with open("all_artists.json", "r") as file:
    all_artists = json.load(file)

# Standardize the data

# Remove duplicates
unique_artists = []
unique_ids = set()
for artist in all_artists:
    if artist["id"] not in unique_ids:
        unique_artists.append(artist)
        unique_ids.add(artist["id"])

# Sort the artists by name
unique_artists.sort(key=lambda artist: artist["name"])

# Write the standardized data to a new JSON file
with open("unique_artists.json", "w") as file:
    json.dump(unique_artists, file, indent=4)

# Remove the original JSON file
# os.remove("all_artists.json")
# The snippet first loads the all_artists.json file and then standardizes the data by removing duplicates and sorting the artists by name. The standardized data is then written to a new JSON file called unique_artists.json. Finally, the original JSON file is removed using the os.remove() function.



