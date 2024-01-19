import controller.control as control
from flask import request
import json

def search_for_artist(token):
    # unpackage json body
    data = json.loads(request.get_data())
    artist_name = data['artist_name']

    # call controller
    result = control.search_for_artist(token, artist_name)

    # package result
    artist_id, artist_name = result['id'], result['name']
    artist = { 'response': [{'artist_id': artist_id}, {'artist_name': artist_name}]}
    response = json.dumps(artist)
    return response

def get_songs_by_artist(token):
    # unpackage json body
    data = json.loads(request.get_data())
    artist_name = data['artist_name']

    # call controller
    result = control.search_for_artist(token, artist_name)
    artist_id = result['id']
    songs = control.get_songs_by_artist(token, artist_id)

    # package result
    song_names = []
    for song in songs:
        song_names.append(song['name'])
    songs = { 'response': {'song_names': song_names} }
    response = json.dumps(songs)
    return response

def get_recommendations_by_artist(token):
    # unpackage json body
    data = json.loads(request.get_data())
    artist_name = data['artist_name']

    # call controller
    result = control.search_for_artist(token, artist_name)
    artist_id = result['id']
    recommendations = control.get_recommendations_by_artist(token, artist_id)

    # package result
    recs = []
    for rec in recommendations:
        recs.append({'song_name': rec['name'], 'artist_name': rec['artists'][0]['name']})
    recs = { 'response': {'recommendations': recs} }
    response = json.dumps(recs)
    return response
