"""
Created on 1/5/20

@author: danielkeidar

Note: Flask app program
"""

# Dependencies
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import sys
import GeniusScrape as gs

# Initialize Flask Framework and Connect Mongo database
app = Flask(__name__)
mongo = PyMongo(app, uri='mongodb://localhost:27017/app')


# Create homepage
@app.route("/")
def home():
    return render_template("index.html", text=user_artist)


@app.route("/", methods=['GET','POST'])
def user_artist():
    artist = request.form['artist']
    albums_urls = gs.track_urls(gs.url_gen(gs.format_name(artist), gs.get_album_list(artist)))
    progress=0
    track_lyrics_list = []
    for index, track in enumerate(albums_urls):
        progress += 1
        track_lyrics_list = gs.track_lyrics(track)
    return render_template('index.html',
                           albums_urls=albums_urls,
                           artist=artist,
                           tracklyrics=track_lyrics_list,
                           progress=progress)

if __name__ == "__main__":
    app.run(debug=True)


