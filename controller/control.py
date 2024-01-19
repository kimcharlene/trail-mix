from requests import get
import json


# TODO: controlling user's player, requires authentication of user
# client vs. user crediential flow

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

def get_auth_header(token):
    # constructing header to be used in requests
    return {"Authorization": "Bearer " + token}