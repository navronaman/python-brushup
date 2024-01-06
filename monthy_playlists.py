import time
import pandas as pd
from findplaylist import Playlist, Song

DF = pd.read_csv("monthly_playlists.csv")

def create_monthly_array(df=DF):
    
    spotify_ids = []
    spotify_playlists = []

    for id in df["ID"]:
        parts = id.split(":")
        spotify_ids.append(parts[-1])
        playlist_i = Playlist(playlist_id=parts[-1])
        spotify_playlists.append(playlist_i)
        
    return spotify_playlists
        
SPOTIFY_PLAYLISTS = create_monthly_array()
    
                    
def what_playlist_what_song(song_id_to_find, spotify_playlists=SPOTIFY_PLAYLISTS):
    
    word = "Song not found"
        
    for playlist in spotify_playlists:
        song_ids = playlist.get_songs_id_array()
        for song in song_ids:
            if song == song_id_to_find:
                print("I'm here!")
                word = word + f"Song found in {playlist.get_playlist_name()}"
                break
            
    return word
    

if __name__ == "__main__":
    
    start_time = time.time()

    song_q = input("Enter song name: ")
    song_to_find = Song(song_q)
    song_id_to_find = song_to_find.get_id()
    
    print(f"Song Name: {song_to_find.get_name()}")
    print(f"Song Artist(s): {song_to_find.get_artists()}")
    
    print(what_playlist_what_song(song_id_to_find=song_id_to_find))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")




