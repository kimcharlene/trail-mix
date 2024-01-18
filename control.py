from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json

from flask import request

# load .env file
load_dotenv()

# load environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# TODO: controlling user's player, requires authentication of user
# client vs. user crediential flow


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


def get_auth_header(token):
    # constructing header to be used in requests
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    # query for first artist that matches result
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query

    result = get(query_url, headers=headers)
    # items holds the data of artist if exists
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists found with this name")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def get_recommendations_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    # query for seed artist
    query = f"seed_artists={artist_id}&limit=10"
    query_url = url + "?" + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


# auth token to be used in all future headers when sending a request
token = get_token()

user_artist_search = input("\nWhich artist are you looking for? ")
result = search_for_artist(token, user_artist_search)

# extract the id given the artist .json
artist_id = result["id"]

# get top tracks of artist
songs = get_songs_by_artist(token, artist_id)
print(f"\nTop 10 Tracks from {result['name']}\n")
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

print(f"\nAnd some recommended tracks related to this artist:\n")
recommendations = get_recommendations_by_artist(token, artist_id)
for idx, rec in enumerate(recommendations):
    print(f"{idx + 1}. {rec['name']} by {rec['artists'][0]['name']}")
print("\n")
