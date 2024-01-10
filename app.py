# This is the Flask app

# From the backend files
from functions import what_playlist_what_song, create_monthly_array 
from backend import Song 

# Imports from flask
from flask import Flask, render_template, request, redirect, jsonify, session

# For the client ID and client Secret
import secrets 
from dotenv import load_dotenv 
import os
import base64

# For the API calls within OAuth 2.0
import requests 
import urllib.parse
import json

# For time
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

MONTHLY_PLAYLISTS = create_monthly_array()

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = "http://localhost:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


@app.route("/")
def index():
        
    return render_template("index.html")

@app.route("/check", methods=["POST", "GET"])
def check(monthly_playlists = MONTHLY_PLAYLISTS):
    
    if request.method == "POST":
    
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
        Song Name: {song_name}
        """
        message_new = f"""
        \n Song Artists: {song_artists}
        """
            
        song_check, play_url = what_playlist_what_song(song_to_find)
        
        audio_message = ""
        playback_link = song_to_find.get_playback()
        
        if playback_link != None:
            audio_message = f"""
            <audio src='{song_to_find.get_playback()}' controls loop preload = 'metadata'>
            
            </audio>
            
            """    
        
            
        return render_template(
                "check.html",
                message1 = message1,
                message_new = message_new,
                naval = song_check,
                song_image_url=song_image_url,
                song_link_url=song_link_url,
                play_url=play_url,
                audio=audio_message
            )
    
    else:
        return render_template("index.html")
        
@app.route('/login')
def login():
    
    scope = "ugc-image-upload playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
    
    # remove show_dialog during execution
    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URL,
        'show_dialog' : True
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args:
        
        req_body = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URL,
            'client_id' : CLIENT_ID,
            'client_secret' : CLIENT_SECRET            
        }
        
        response = requests.post(url=TOKEN_URL, data=req_body)
        token_info = json.loads(response.content)
        
        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]
        
        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect('/refresh-token')
    
    if 'access_token' in session or datetime.now().timestamp() > session["expires_at"]:
    
        headers = {
            'Authorization' : f"Bearer {session['access_token']}"
        }
        
        result = requests.get(url="https://api.spotify.com/v1/me/playlists", headers=headers)
        playlists = json.loads(result.content)
        
        #return jsonify(playlists)
        
        return render_template("homepage.html")
    
    else:
        return jsonify({"HELLO" : "I NEED HELP"})
        
@app.route('/refesh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session["expires_at"]:
        req_body = {
            'grant_type' : 'refresh_token',
            'refresh_token' : session['refresh_token']
        }
        
        auth_string = CLIENT_ID + ":" + CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        
        header = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        
        result = requests.post(url=AUTH_URL, headers=header, data=req_body)
        
        new_token_info = json.loads(result.content)
        
        session["access_token"] = new_token_info["access_token"]
        session["refresh_token"] = new_token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + new_token_info["expires_in"]
        
        return redirect('/playlist')
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)