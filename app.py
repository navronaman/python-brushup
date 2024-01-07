# This is the Flask app
from flask import Flask, render_template, request, flash
from monthy_playlists import what_playlist_what_song, create_monthly_array
from findplaylist import Song
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

MONTHLY_PLAYLISTS = create_monthly_array()

@app.route("/")
def index():
    
    flash(message="What song buddy?")
    
    return render_template("index.html")

@app.route("/check", methods=["POST", "GET"])
def check(monthly_playlists = MONTHLY_PLAYLISTS):
    song_name = str(request.form["song_input"])
    song_to_find = Song(song_name)
    
    song_name = song_to_find.get_name()
    song_artists_list = song_to_find.get_artists()
    song_artists = ""
    
    if len(song_artists_list) == 1:
        song_artists = song_artists_list[0]
    else:
        for index, artist in enumerate(song_artists_list):
            song_artists += artist
            if index < len(song_artists_list) - 1:
                song_artists += ", "
    
    song_image_url = song_to_find.get_image_url()
    song_link_url = song_to_find.get_song_url()
    
    message1 = f"""
    Song Name: {song_name} \t
    \n Song Artists: {song_artists}
    """
        
    song_check, play_url = what_playlist_what_song(song_to_find)
    
    audio_message = ""
    playback_link = song_to_find.get_playback()
    
    if playback_link != "null" or playback_link != "None":
        audio_message = f"""
        <audio src='{song_to_find.get_playback()}' controls loop preload = 'metadata'>
        
        </audio>
        
        """    
    
        
    return render_template("check.html", message1 = message1, naval = song_check, song_image_url=song_image_url, song_link_url=song_link_url, play_url=play_url, audio=audio_message)
    

if __name__ == "__main__":
    app.run(host="120.0.0.1", port=0000, debug=True)