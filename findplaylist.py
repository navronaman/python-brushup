import requests
import os
from dotenv import load_dotenv
import base64
import json

# We will try to get one playlists from the user first

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token_cc():
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
        
    result = requests.post(url=url, headers=header, data=form)
    json_result =  json.loads(result.content)
    
    token = json_result["access_token"]
    return token


token = get_token_cc()

def get_auth_header_cc(token):
    return {
        "Authorization" : "Bearer " + token
    }
    
header_auth = get_auth_header_cc(token=token)

PLAYLIST_ID = "5KGUSMWkfWedc067zW7BYM"
GET_PLAYLIST_URL = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}"


def get_playlist(playlist_id, fields, market="US"):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header_cc(token=token)
    
    query = f"?fields={fields}&market={market}"
            
    query_url = url + query
    
    result = requests.get(url=query_url, headers=headers)

    json_result = json.loads(result.content)
    
    return json_result

def get_user_playlist(limit=50, offset=10):
    url = f"https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header_cc(token)
    query = f"?limit={limit}&offset={offset}"
    
    query_url = url + query
    
    result = requests.get(url=query_url, headers=headers)
    
    json_result = json.loads(result.content)
    
    return json_result
    


if __name__ == "__main__":
    json1 = get_playlist("5KGUSMWkfWedc067zW7BYM", "images")
    print(json1["images"][0]["url"])
    
    json2 = get_user_playlist()
    print(json2)
    


