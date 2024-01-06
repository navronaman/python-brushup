# This is the Flask app
from flask import Flask, render_template, request, flash
from monthy_playlists import what_playlist_what_song, create_monthly_array
from findplaylist import Song
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

MONTHLY_PLAYLISTS = create_monthly_array()

@app.route("/")

def trial():
    return "Hello World"

@app.route("/index")
def index():
    
    flash(message="What song buddy?")
    
    return render_template("index.html")

@app.route("/check", methods=["POST", "GET"])
def check(monthly_playlists = MONTHLY_PLAYLISTS):
    song_name = str(request.form["song_input"])
    song_to_find = Song(song_name)
    song_id = song_to_find.get_id()
    
    song_name = song_to_find.get_name()
    song_artists = song_to_find.get_artists()
    song_image_url = song_to_find.get_image_url()
    song_link_url = song_to_find.get_song_url()
    
    message1 = f"""
    Song Name: {song_name} \t
    \n Song Artists: {song_artists}
    """
    
    flash(message=message1)
    
    song_check = what_playlist_what_song(song_id)
    
    flash(song_check, "song_check")
    
    return render_template("check.html", song_image_url=song_image_url, song_link_url=song_link_url)
    

if __name__ == "__main__":
    app.run(host="120.0.0.1", port=8080, debug=True)