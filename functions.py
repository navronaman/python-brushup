import time
start_time = time.time()
import pandas as pd
import random
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
    
def random_playlist_obj(json_file):
    
    try:
        
        print("I'm at option 1")
        
        random_index = random.randint(0, len(json_file["items"]))
        
        playlist_return = Playlist(playlist_id=json_file["items"][random_index]["uri"].split(":")[-1])
        
    except (KeyError, IndexError):
        
        print("I'm at option 2")
                
        playlist_return = Playlist(playlist_id=json_file["items"][0]["uri"].split(":")[-1])
        
    return playlist_return

def top_task1(top, search, time):
    
    match top:
        case 0:
            top_var = "Top 10"
            tv1 = 10
        case 1:
            top_var = "Top 50"
            tv1 = 50
        case _:
            top_var = "Top 10"
            tv1 = 10
            
    match search:
        case 0:
            search_var = "tracks"
            sv = "tracks"
        case 1:
            search_var = "artists"
            sv = "artists"
        case 2:
            search_var = "genres"
            sv = "artists" # needs work
        case _:
            search_var = "tracks"
            sv = "tracks"
            
    match time:
        case 0:
            time_var = "in the last month"
            tv2 = "short_term"
        case 1:
            time_var = "in the last 6 months"
            tv2 = "medium_term"
        case 2:
            time_var = "in your lifetime"
            tv2 = "long_term"
            
    url = f"https://api.spotify.com/v1/me/top/{sv}?time_range={tv2}&limit={tv1}"
    msg = f"Here are your {top_var} {search_var} {time_var}"
    
    return msg, url
        
            
    
def top_task2(json_file):
    
    try:
                
        if json_file["href"].split("/")[-1].startswith("tracks"):
            
            main_d = {index + 1: [trackdict['name'], trackdict['album']['name']] for index, trackdict in enumerate(json_file["items"])}
            
            text_r = """
            <table border="1">
                <tr>
                    <th>No.</th>
                    <th>Song Name</th>
                    <th>Album Name</th>
                </tr>
            """
            
            for index, song_obj in main_d.items():
                text_r += f"""
                <tr>
                    <td>{index}</td>
                    <td>{song_obj[0]}</td>
                    <td>{song_obj[1]}</td>
                </tr>
                """
                
                if index == len(main_d):
                    text_r += """
                    </table>                                        
                    """
        
            return text_r
        
        else:
            
            main_d = {index+1 : artist['name'] for index, artist in enumerate(json_file["items"])}
            
            text_r = """
            <table border="1">
                <tr>
                    <th>No.</th>
                    <th>Artist Name</th>
                </tr>
            """
            
            for index, art_obj in main_d.items():
                text_r += f"""
                <tr>
                    <td>{index}</td>
                    <td>{art_obj}</td>
                </tr>
                """
                
                if index == len(main_d):
                    text_r += """
                    </table>                                        
                    """
                    
            return text_r
        
    except Exception as e:
        
        return str(e)
    

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




