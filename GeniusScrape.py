"""
Created on 1/5/20

@author: danielkeidar

Note: Scrape Genius.com for artist lyrics
"""
from bs4 import BeautifulSoup
import requests
import json
import os
import random


def user_agent():
    directory = os.getcwd()
    with open(directory + r'/user_agent.json', 'r') as file:
        agent = json.load(file)
    return agent[random.randint(1, len(agent))]


class GeniusScrape:

    def __init__(self, user_artist):
        self.artist = user_artist

    # removing characters to fit the formatting of Genius.com URL Structure
    def format_artist(self):
        artist_f = self.replace(' ', '-').replace('.', '').replace("'", '').replace('$', '-').lower()
        return artist_f

    def url_gen(self):
        geniusurl = 'https://wwww.genius.com/'

