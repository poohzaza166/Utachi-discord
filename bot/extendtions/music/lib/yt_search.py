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
import re
from pprint import pprint

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from ....log import logs
from .key import ApiKeys

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main(querry : str):
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


        request = youtube.search().list(
            part="snippet",
            order="relevance",
            q=querry,
            safeSearch="none",
            maxResults=1,
            videoCaption="any",
            videoType="any"
        )
        response = request.execute()
        return response

    try:
        response = run()
    except HttpError as err:
        logs.info('apikey max limit reach')
        if err.status_code == 403:
            ApiKeys.changekey()
            response = run()

    try:
        vidlink = "https://www.youtube.com/watch?v=" + response['items'][0]['id']['videoId']
    except:

        return False
    return vidlink

if __name__ == "__main__":
    main('unlasting')
