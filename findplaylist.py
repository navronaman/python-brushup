import requests
import os
from dotenv import load_dotenv
import base64
import json

# We will try to get one playlists from the user first

load_dotenv()

PLAYLIST_ID = "5KGUSMWkfWedc067zW7BYM"
GET_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
        
    form = {
        "grant_type": "client_credentials"
    }
    
    # We will be sending a Post request 
    
    auth_options = {}
    
    result = requests.post(url=url, headers=header, data=form)
    json_result =  json.load(result.content)
    
    token = json_result["access_token"]
    return token

    
    
    



