from flask import Flask

# create instance of flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Trail Mix API!"

@app.route("artist/top_tracks")
def artist_top_tracks():
    return f'Top tracks'

@app.route("artist/recommendations")
def recommendations_by_artist(artist):
    return 'Recommendations'