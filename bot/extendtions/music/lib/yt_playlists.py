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

# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from pprint import pprint
from time import sleep

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from ....log import logs
from .key import ApiKeys

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

class yt_playlist:
    def __init__(self):
        self.playlist = []

    def main(self, querry : str, page_token=None):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        # Get credentials and create an API client
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        #     client_secrets_file, scopes)
        # credentials = flow.run_console()
        def run():
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=ApiKeys.getkey())

            request = youtube.playlistItems().list(
                part="contentDetails,status",
                playlistId=querry,
                maxResults=50,
                pageToken=page_token
            )
            response = request.execute()
            return response

        try:
            response = run()
        except HttpError as err:
            if err.status_code == 403:
                ApiKeys.changekey()
                response = run()
            if err.status_code == 404:
                raise Exception('Video Not found')

        for n in response['items']:
            if n['status']['privacyStatus'] == 'private':
                logs.info('found privated video')
            else:
                self.playlist.append('https://www.youtube.com/watch?v=' + n['contentDetails']['videoId'])

        if 'nextPageToken' in response:
            return response['nextPageToken']
        else:
            pass

    # def run_thread(self, url, why):
    #     print(why)
    #     return self.parse_data(url)

    def parse_data (self,url):
        """get all video url inside of playlist

        Args:
            url strting: url of the playlist

        Returns:
            list: video url of the playlist
        """
        try:
            querry = url.replace('https://www.youtube.com/playlist?list=','')
            s = True
            c = False
            while s == True:
                if c == False:
                    c = self.main(querry)
                elif type(c) == str:
                    c = self.main(querry,c)
                elif c == None:
                    s = False
                    break
            return self.playlist.copy()
            
        except Exception as a:
            print('test')
            logs.error(a)
        finally:
            self.playlist.clear()



if __name__ == "__main__":
    parse_data('PLKu0PlxNFnZUjUzSxccTzHOgEYYGlSJk5')
    print(len(playlist))
