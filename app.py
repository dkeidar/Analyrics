"""
Created on 1/5/20

@author: danielkeidar

Note: Flask app program
"""

# Dependencies
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import sys
from GeniusScrape import GeniusScrape as gs

# Initialize Flask Framework and Connect Mongo database
app = Flask(__name__)
mongo = PyMongo(app, uri='mongodb://localhost:27017/app')


# Create homepage
@app.route("/")
def home():
    return render_template("index.html", text=user_artist)


@app.route("/", methods=['POST'])
def user_artist():
    artist = request.form['artist']
    artist_f = gs.format_artist(artist)
    return redirect(f"/?artist={artist_f}")


def artist_scrape():
    return gs.scrape(user_artist)


if __name__ == "__main__":
    app.run(debug=True)


