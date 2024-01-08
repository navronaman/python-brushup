import requests
import os
from dotenv import load_dotenv
import base64
import json

# We will try to get one playlists from the user first

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = "http://localhost:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_auth_header_cc():
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
    
    if result.status_code == 200:
        json_result =  json.loads(result.content)
        token = json_result["access_token"]
        
        return {
            "Authorization" : "Bearer " + token
        }
        
    else:
        print("Error with headers")
        return "Invalid"
    
    
    
class Song:
    def __init__(self, query_word):
        self.query = query_word
        self.track_item = self.get_song_from_search_json()
        
    def get_name(self):
        try:
            return self.track_item["name"]
        except KeyError:
            return "Never Gonna Let You Down"
        
    
    def get_id(self):
        try:
            return self.track_item["id"]
        except KeyError:
            return "OlaAmigo"
        
    def get_album_name(self):
        try:
            return self.track_item["album"]["name"]
        except KeyError:
            return "Jhalak Dikhlaja"
             
        
    def get_song_from_search_json(self):
        url = "https://api.spotify.com/v1/search"
        headers = get_auth_header_cc()
        
        updated_song = ""
        for char in self.query:
            if char == " ":
                updated_song += "+"
            else:
                updated_song += char

                    
        query = f"?q={updated_song}&type=track&market=US&limit=1&offset=0"
        
        query_url = url + query
        
        if type(headers) != str:
            result = requests.get(url=query_url, headers=headers)
            
            json_result = json.loads(result.content)
            
            try:
                track_item_json = json_result["tracks"]["items"][0]
                
            except (KeyError, IndexError):
                track_item_json = json_result
            
            return track_item_json
        
        else:
            return {404: "Error"}
        
    def get_artists(self):
        artists = []
        try:
            for index, value in enumerate(self.track_item["artists"]):
                for k, c in self.track_item["artists"][index].items():
                    if k == "name":
                        artists.append(c)
                        continue
                    
            return artists
            
        except (KeyError, IndexError):
            return "Himesh R"
            
    def get_image_url(self):
        
        try:
            return self.track_item["album"]["images"][0]["url"]
        
        except (KeyError, IndexError):
            return "https://i.scdn.co/image/ab67616d0000b273048705b0425dcf3dbacbc49a"
    
    def get_song_url(self):
        
        try:
            song_url = self.track_item["external_urls"]["spotify"]
        
        except KeyError:
            
            try:         
                song_url = self.track_item["album"]["external_urls"]["spotify"]
                
            except KeyError:
                song_url = "https://youtu.be/dQw4w9WgXcQ?si=IGFC0ZxLDrACyJxg"
        
        return song_url
    
    def get_playback(self):
        
        try:
            playback_url = self.track_item["preview_url"]
        except KeyError:
            playback_url = "null"
            
        return playback_url
            
            
        

# Let's get a song from a search query
class Playlist:
    def __init__(self, playlist_id, market="US"):
        self.playlist_id = playlist_id
        self.market = market
        self.playlist_json = self.get_json_playlist()
                
    def get_json_playlist(self):
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
        headers = get_auth_header_cc()
        
        query = f"?market={self.market}"
                
        query_url = url + query
        
        if type(headers) != str:

            result = requests.get(url=query_url, headers=headers)

            json_result = json.loads(result.content)
            
            return json_result
        
        else:
            
            return {404 : "Another error"}
        
    def get_playlist_name(self):
        try:
            return self.playlist_json["name"]
        except KeyError:
            return "Error"
    
    def get_playlist_ownder(self):
        try:
            return self.playlist_json["owner"]["display_name"]
        except KeyError:
            return "Error"
    
    def get_playlist_url(self):
        try:
            return self.playlist_json["external_urls"]["spotify"]
        except KeyError:
            return "Error"
    
    def get_songs_array(self):
        
        tmp = []
        
        try:                
            for index, track_dict in enumerate(self.playlist_json["tracks"]["items"]):
                for k, c in self.playlist_json["tracks"]["items"][index].items():
                    if k == "track":
                        for i, j in self.playlist_json["tracks"]["items"][index][k].items():
                            if i == "name":
                                tmp.append(j)
                                continue
                            
        except (KeyError, IndexError):
            tmp = ["Never Gonna Give You Up"]
                            
        return tmp
                        
    def get_songs_id_array(self):
        
        tmp = []
        
        try:               
            for index, track_dict in enumerate(self.playlist_json["tracks"]["items"]):
                for k, c in self.playlist_json["tracks"]["items"][index].items():
                    if k == "track":
                        for i, j in self.playlist_json["tracks"]["items"][index][k].items():
                            if i == "id":
                                tmp.append(j)
                                continue
                            
        except (KeyError, IndexError):
            tmp = ["Never Gonna Let You Down"]

        return tmp
    
    def print_songs(self):
        
        song_list = self.get_songs_array()
        for index, song in enumerate(song_list):
            print(f"\n {index+1}. {song}")
                        
    def most_featured_artist(self):
                
        tmp = []
        
        try:
        
            for index, track_dict in enumerate(self.playlist_json["tracks"]["items"]):
                for k, c in self.playlist_json["tracks"]["items"][index].items():
                    if k == "track":
                        for ai, artist in enumerate(self.playlist_json["tracks"]["items"][index][k]["artists"]):
                            for i, j in self.playlist_json["tracks"]["items"][index][k]["artists"][ai].items():
                                if i == "name":
                                    tmp.append(j)
                                    continue
                                
            mfartist = tmp[0]
            max_occ = 0
            
            for artist in tmp:
                occurences = tmp.count(artist)
                if occurences > max_occ:
                    max_occ = occurences
                    mfartist = artist
                    
            return mfartist, max_occ
        
        except (KeyError, IndexError):
            
            return "Himesh Resh", 20000
        
    def most_featured_album(self):
        
        tmp = []
        
        try:
        
            for index, track_dict in enumerate(self.playlist_json["tracks"]["items"]):
                for k, c in self.playlist_json["tracks"]["items"][index].items():
                    if k == "track":
                        for album_key, album_v in self.playlist_json["tracks"]["items"][index][k]["album"].items():
                            if album_key == "name" and album_v != "":
                                tmp.append(album_v)
                                continue
                                
            mfalbum = tmp[0]
            max_occ = 0
            
            for album in tmp:
                occurences = tmp.count(album)
                if occurences > max_occ:
                    max_occ = occurences
                    mfalbum = album
                    
            return mfalbum, max_occ
        
        except (KeyError, IndexError):
            
            return "Tandoori Nights", 20000
        
    def is_song_in_playlist(self, song_to_check):
        id_to_check = song_to_check.get_id()
        
        b = False
        
        for index, track_dict in enumerate(self.playlist_json["tracks"]["items"]):
            for k, c in self.playlist_json["tracks"]["items"][index].items():
                if k == "track":
                    if self.playlist_json["tracks"]["items"][index][k]["id"] == id_to_check:
                        b = True
                        break
                    
        return b
                
    
                    
# For the get playlist code, we need better OAuth code, let's work with a search query
def get_user_playlist(limit=50, offset=10):
    url = f"https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header_cc()
    query = f"?limit={limit}&offset={offset}"
    
    query_url = url + query
    
    result = requests.get(url=query_url, headers=headers)
    
    json_result = json.loads(result.content)
    
    return json_result
    


if __name__ == "__main__":
    
    print("\n")
    
    playlist1 = Playlist(playlist_id="5KGUSMWkfWedc067zW7BYM")
    print(playlist1.get_playlist_name())
    playlist1.print_songs()    

    print("\n")
    
    print(playlist1.most_featured_artist())
    print(playlist1.most_featured_album())
        
    print(playlist1.is_song_in_playlist(Song("Haan Main Galat")))
    print(playlist1.is_song_in_playlist(Song("Haule Haule")))
    
    print("\n")

    
    song1 = Song(query_word="my darkest hours girl i felt so alone")
    print(song1.get_name())
    print(song1.get_artists())
    print(song1.get_id())
    


