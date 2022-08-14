from time import sleep
from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from ....fileio import botconfig
from . import yt_search

from ....log import logs

auth_manager = SpotifyClientCredentials(client_id=botconfig['bot_setting']['spotipyid'],client_secret=botconfig['bot_setting']['spotipysc'])
sp = spotipy.Spotify(auth_manager=auth_manager)

setlist = []

def main(id, offset = None):
    playlists = sp.playlist_tracks(id,offset=offset)
    try:
        for n in playlists['tracks']['items']:
            name = n['track']['name']
            author = n['track']['artists'][0]['name']
            searchq = name + ' by ' + author
            setlist.append(yt_search.main(searchq))
        if playlists['tracks']['next'] == None:
            return 'null'
        else:
            return len(playlists['tracks']['items']) , playlists['tracks']['total']
    except KeyError:
        for n in playlists['items']:
                name = n['track']['name']
                author = n['track']['artists'][0]['name']
                searchq = name + ' by ' + author
                setlist.append(yt_search.main(searchq))
        if playlists['next'] == None:
            return 'null'
        else:
            return len(playlists['items']) , playlists['total']

def parse_data(url):
    querry = url.replace('https://open.spotify.com/playlist/', '')
    s = True
    c = False
    v = 0
    while s == True:
        if type(c) == bool:
            try:
                a,v = main(querry)
                c = 0
            except ValueError:
                break
        elif type(c) == int:
            try:
                a,v = main(querry,c)
                if (c + a) - v == 0:
                    s = False
                    break
                else:
                    limit = c + a
                    c = limit
            except TypeError:
                s = False
                break
    sleep(1)
    return setlist


if __name__ == "__main__":
    parse_data('https://open.spotify.com/playlist/4Dg0J0ICj9kKTGDyFu0Cv4')

