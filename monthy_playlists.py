import time

start_time = time.time()

import pandas as pd
from findplaylist import Playlist, Song

df = pd.read_csv("monthly_playlists.csv")

spotify_ids = []
SPOTIFY_PLAYLISTS = []

for id in df["ID"]:
    parts = id.split(":")
    spotify_ids.append(parts[-1])
    playlist_i = Playlist(playlist_id=parts[-1])
    SPOTIFY_PLAYLISTS.append(playlist_i)
    
song_q = input("Enter song name: ")
song_to_find = Song(song_q)
song_id_to_find = song_to_find.get_id()

print(f"Song Name: {song_to_find.get_name()}")
print(f"Song Artist(s): {song_to_find.get_artists()}")

for playlist in SPOTIFY_PLAYLISTS:
        song_ids = playlist.get_songs_id_array()
        for song in song_ids:
            if song == song_id_to_find:
                print(f"Song found in {playlist.get_playlist_name()}")
                break
            
print(song_id_to_find)
        
def what_playlist_what_song(song_id_to_find):
    
    str = ""
        
    for playlist in SPOTIFY_PLAYLISTS:
        song_ids = playlist.get_songs_id_array()
        for song in song_ids:
            if song == song_id_to_find:
                print("I'm here!")
                str = str + f"Song found in {playlist.get_playlist_name()}"
                break
            
    return str
    
print(what_playlist_what_song("Superman"))
    
    

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")