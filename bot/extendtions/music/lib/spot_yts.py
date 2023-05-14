# Copyright 2023 pooh
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pprint import pprint
from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from ....fileio import botconfig
from ....log import logs
from . import yt_search

auth_manager = SpotifyClientCredentials(client_id=botconfig['bot_setting']['spotipyid'],client_secret=botconfig['bot_setting']['spotipysc'])
sp = spotipy.Spotify(auth_manager=auth_manager)

class spot_yt:
    def __init__(self):
        self.setlist = []

    def main(self, id, offset = None):
        playlists = sp.playlist_tracks(id,offset=offset)
        try:
            for n in playlists['tracks']['items']:
                name = n['track']['name']
                author = n['track']['artists'][0]['name']
                searchq = name + ' by ' + author
                self.setlist.append(yt_search.main(searchq))
            if playlists['tracks']['next'] == None:
                return 'null'
            else:
                return len(playlists['tracks']['items']) , playlists['tracks']['total']
        except KeyError:
            for n in playlists['items']:
                    name = n['track']['name']
                    author = n['track']['artists'][0]['name']
                    searchq = name + ' by ' + author
                    self.setlist.append(yt_search.main(searchq))
            if playlists['next'] == None:
                return 'null'
            else:
                return len(playlists['items']) , playlists['total']

    # def run_thread(self, url,why):
    #     print(why)
    #     return self.parse_data(url=url)

    def parse_data(self, url):
        try:
            querry = url.replace('https://open.spotify.com/playlist/', '')
            s = True
            c = False
            v = 0
            while s == True:
                if type(c) == bool:
                    try:
                        a,v = self.main(querry)
                        c = 0
                    except ValueError:
                        break
                elif type(c) == int:
                    try:
                        a,v = self.main(querry,c)
                        if (c + a) - v == 0:
                            s = False
                            break
                        else:
                            limit = c + a
                            c = limit
                    except TypeError:
                        s = False
                        break
            return self.setlist.copy()
        except Exception as a:
            logs.error(a)
        finally:
            self.setlist.clear()

if __name__ == "__main__":
    parse_data('https://open.spotify.com/playlist/4Dg0J0ICj9kKTGDyFu0Cv4')

