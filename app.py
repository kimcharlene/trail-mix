from flask import Flask
import json

from view.view import *

from dotenv import load_dotenv
from requests import post
import os
import base64

# create instance of flask
app = Flask(__name__)

# load .env file
load_dotenv()

# load environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    # creating authorization string with base64 encoding
    # to retrieve authorization token

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # url to write requests to
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # send a POST request
    result = post(url, headers=headers, data=data)
    # returned a .json in content
    json_result = json.loads(result.content)
    # parse out the token
    token = json_result["access_token"]
    return token


# auth token to be used in all future headers when sending a request
token = get_token()

@app.route("/")
def start_page():
    return "Trail Mix API!"

# return artist's id and name
@app.route("/artist", methods=["POST"])
def find_artist():
    return search_for_artist(token)

@app.route("/artist/top_tracks", methods=["POST"])
def artist_top_tracks():
    return get_songs_by_artist(token)

@app.route("/artist/recommendations", methods=["POST"])
def recommendations_by_artist():
    return get_recommendations_by_artist(token)

