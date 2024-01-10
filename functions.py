import time
start_time = time.time()
import pandas as pd
from backend import Playlist, Song

DF = pd.read_csv("monthly_playlists.csv")

def create_monthly_array(df=DF):
    
    # We make an array of Playlist objects using the database spotify IDs
        
    return [Playlist(playlist_id=x.split(":")[-1]) for x in df["ID"]]
        
SPOTIFY_PLAYLISTS = create_monthly_array()
    
                    
def what_playlist_what_song(song_to_find, spotify_playlists=SPOTIFY_PLAYLISTS):
        
    booboo = False
    word = ""
    url = ""
        
    for playlist in spotify_playlists:
        
        if playlist.is_song_in_playlist(song_to_find):
            playlist_extreme = playlist
            booboo = True
            break            
            
    if booboo:
        word = f"Song is found in {playlist_extreme.get_playlist_name()}"
        url = f"{playlist_extreme.get_playlist_url()}"
        
    else:
        word = f"Song is found in {song_to_find.get_album_name()}"
        url = f"{song_to_find.get_song_url()}"
            
    return word, url
    

if __name__ == "__main__":
    
    song_q = input("Enter song name: ")
    song_to_find = Song(song_q)
    
    print(f"Song Name: {song_to_find.get_name()}")
    print(f"Song Artist(s): {song_to_find.get_artists()}")
    
    word, url = what_playlist_what_song(song_to_find)
    print(word)
    print(url)
    print(song_to_find.get_playback())
    print(type(song_to_find.get_playback()))

    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")




