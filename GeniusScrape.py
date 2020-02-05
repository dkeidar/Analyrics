"""
Created on 1/5/20

@author: danielkeidar

Note: Scrape Genius.com for artist lyrics
"""
# Libraries for scraping Genius.com
from bs4 import BeautifulSoup
import requests
import json
import os
import random
# Spotify API python wrapper
import spotipy
import spotipy.oauth2 as oauth2
import config
# NLP Libraries
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import re
import pandas as pd


def user_agent():
    directory = os.getcwd()
    with open(directory + r"/user_agent.json", "r") as file:
        agent = json.load(file)
    return agent[random.randint(1, len(agent))]


header = user_agent()


def spotify_auth():
    client_id = config.sp_CLIENT_ID
    client_secret = config.sp_CLIENT_SECRET
    credentials = oauth2.SpotifyClientCredentials(client_id=client_id,
                                                  client_secret=client_secret)
    token = credentials.get_access_token()
    sp = spotipy.Spotify(auth=token)
    return sp


# removing characters to fit the formatting of Genius.com URL Structure
def format_name(user_artist):
    punct = [(" ", "-"), (".", "-"), ("'", "-"), ("(", "-"), (")", "-version"), (",", "-")]
    name = user_artist.lower()
    for k, v in punct:
        name = name.replace(k, v)
        if "--" in name:
            name = name.replace("--", "-")
        if name.endswith("-"):
            name = name[:-1]
    return name


# generate a list of albums by the artist using the spotify api
def get_album_list(user_artist):
    sp = spotify_auth()

    artist_search = sp.search(q=f"{user_artist}", type="artist")
    artist_id = artist_search["artists"]["items"][0]["id"]

    album_list = []
    album_search = sp.artist_albums(artist_id, album_type="album", limit=50)
    for i in range(len(album_search["items"])):
        album = album_search["items"][i]["name"]
        if album not in album_list:
            album_list.append(album)
    return album_list


def url_gen(artist_f, album_list):
    geniusurl = "https://www.genius.com/albums/"
    urllist = list()

    mid_url = f'{geniusurl}{artist_f}'

    for album in album_list:
        album_f = format_name(album)
        fin_url = f"{mid_url}/{album_f}"
        album_url_dict = {"album_name": album,
                          "url": fin_url}
        urllist.append(album_url_dict)

    return urllist


def track_urls(album_url_dict):
    updated_dict = []
    for album in album_url_dict:
        url = album["url"]
        soup = BeautifulSoup(requests.get(url, headers=header).content, "lxml")
        track_html = soup.find_all("div", {"class": "chart_row-content"})
        for track in track_html:
            track_url = track.a.get("href")
            data = {"album_name": album["album_name"],
                    "album_url": url,
                    "track_url": track_url}
            updated_dict.append(data)
    return updated_dict


def track_lyrics(track):
    track_lyrics_list = []
    song = BeautifulSoup(requests.get(track["track_url"], headers=header).content, "lxml")
    lyricstext = song.find("div", {"class": "lyrics"})
    try:
        track_lyrics_list.append((track["album_name"],
                                  track["album_url"],
                                  song.h2.text.replace("\n", ""),
                                  track["track_url"],
                                  song.h1.text,
                                  lyricstext.find("p").text.replace("\n", "")))
    except ValueError:
        track_lyrics_list.append((track["album_name"],
                                  track["album_url"],
                                  song.h2.text.replace("\n", ""),
                                  track["track_url"],
                                  song.h1.text,
                                  "No Lyrics Available"))
    return track_lyrics_list


def clean_lyrics(track_lyrics_df):
    tokenizer = RegexpTokenizer(r'\w+|\d+')
    lemmatizer = WordNetLemmatizer()

    cleaned = track_lyrics_df.lyrics.apply(lambda x: re.sub(r"\[(.*?)\]", ' ', x))
    tokenized = cleaned.apply(lambda x: tokenizer.tokenize(x.lower().replace("'", '').replace('.', '')))
    lemmatized = tokenized.apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
    no_stops = lemmatized.apply(lambda x: [word for word in x if word not in stopwords.words('english')])
    return no_stops


def word_freqs(track_lyrics_df, ngram='unigram', topwords=50):
    word_list = []
    for row in track_lyrics_df.lyrics_cleaned:
        for word in row:
            word_list.append(word)
        word_list.append("songend")
    if ngram == 'unigram':
        counted = [str(word) for word in word_list if word != "songend"]
    elif ngram == 'bigram':
        counted = ngrams(word_list, 2)
        counted = [str(word) for word in counted if "songend" not in word]
    elif ngram == 'trigram':
        counted = ngrams(word_list, 3)
        counted = [str(word) for word in counted if "songend" not in word]
    else:
        print("try again")
        pass
    dist = FreqDist(counted).most_common(topwords)
    distdf = pd.DataFrame(dist, columns=['term', 'count']).set_index('term')
    return distdf
