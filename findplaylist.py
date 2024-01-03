"""
What is the point of this program?

We have all the playlists from the user, and the song inputted is checked as to see what playlist it is in
"""

import requests
import os
from dotenv import load_dotenv

# We will try to get one playlists from the user first

load_dotenv()

PLAYLIST_ID = "5KGUSMWkfWedc067zW7BYM"
GET_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print(CLIENT_ID, CLIENT_SECRET)







