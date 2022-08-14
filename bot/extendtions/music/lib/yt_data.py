# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
from time import sleep
from pprint import pprint

import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

from .key import ApiKeys
from .ryd import makereq
from ....log import logs

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

        request = youtube.videos().list(
            part="snippet,statistics",
            id=querry,
            maxResults=1
        )
        response = request.execute()
        return response

    try:
        response = run()
    except HttpError as err:
        if err.status_code == 403:
            ApiKeys.changekey()
            response = run()

    return response

def parse_data(url):
    """_summary_

    Args:
        url (string): url of the youtube video

    Returns:
        dict: avaialbe key videoname return str
        bych return str name of youtube channel
        view return int youtube video view count
        like return int like count of the video
        url return str the orginal video url
        chlink return str link of the video publisher channel
    """
    if 'https://music.youtube.com/watch?v=' in url:
        vidid = url.replace('https://music.youtube.com/watch?v=','')
    else:
        vidid = url.replace('https://www.youtube.com/watch?v=', '')
    response = main(vidid)
    sleep(int(0.3))
    logs.debug(response)
    if 0 in response['items']:
        raise Exception('api error')
    redict = {}
    try:
        redict.setdefault('videoname', str(response['items'][0]['snippet']['title']))
        redict.setdefault('bych', str(response['items'][0]['snippet']['channelTitle']))
        redict.setdefault('view', str(response['items'][0]['statistics']['viewCount']))
        redict.setdefault('like', str(response['items'][0]['statistics']['likeCount']))
        redict.setdefault('dislike' ,makereq(url))
        redict.setdefault('url' ,url)
        redict.setdefault('chlink', str('https://www.youtube.com/channel/' + response['items'][0]['snippet']['channelId']))
        return redict
    except IndexError as a:
        logs.debug(a)
        redict.setdefault('videoname', 'video privated or channel deleated')
        redict.setdefault('bych',  'video privated or channel deleated')
        redict.setdefault('view',  'video privated or channel deleated')
        redict.setdefault('like',  'video privated or channel deleated')
        redict.setdefault('dislike' , 'video privated or channel deleated')
        redict.setdefault('url' ,url)
        redict.setdefault('chlink',  'video privated or channel deleated')
        return redict


if __name__ == "__main__":
    test = parse_data("https://www.youtube.com/watch?v=du10-NshNHo")
    print('')
    print('-------------------------------------------------')
    pprint(test)
