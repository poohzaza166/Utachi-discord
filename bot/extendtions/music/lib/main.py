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

import random
import threading

from ytmusicapi import YTMusic

# coding:utf-8
from ....log import logs
from . import yt_data, yt_search
from .spot_yts import spot_yt
from .yt_playlists import yt_playlist
from ....errors import insertPlaylist, noVideoFound

ytmusic = YTMusic()

class musicss:

    def __init__(self):
        self.queue = {}
        self.history = {}
        self.isinfiteloop = {}
        self.currentsong = {}
        self.yt_playlist = yt_playlist()
        self.spot_yt = spot_yt()

    def add_song(self, guildid ,url: str, platform='youtube'):
        platform_list = ['https://www.youtube.com', 'https://music.youtube.com/watch?v=']
        if "https://www.youtube.com/playlist?list=" in url:
            from multiprocessing.pool import ThreadPool
            pool = ThreadPool(processes=1)

            async_result = pool.apply_async(self.yt_playlist.parse_data, [url]) # tuple of args for foo

            # do some other stuff in the main process

            self.queue.setdefault(guildid, []).extend(async_result.get())
            logs.debug('it a playlist')

        elif 'https://youtu.be/' in url:
            rename = url.replace('https://youtu.be/','')
            fullname = 'https://www.youtube.com/watch?v=' + rename
            self.queue.setdefault(guildid, []).append(fullname)
            logs.debug('it a youtube short link')

        elif 'https://music.youtube.com/playlist?list=OLAK5uy_' in url:
            logs.debug('it a youtube music alblum')
            idn = url.replace('https://music.youtube.com/playlist?list=','')
            a = ytmusic.get_album_browse_id(idn)
            b = ytmusic.get_album(a)
            logs.debug('it a youtube music playlist')
            for d in b['tracks']:
                x = d['videoId']
                f = 'https://music.youtube.com/watch?v=' + x
                self.queue.setdefault(guildid, []).append(f)

        elif 'https://open.spotify.com/playlist/' in url:
            logs.debug('converting spotify playlist')
            # detatch the spoitify process from normal process since it block voice chat heart beat
            from multiprocessing.pool import ThreadPool
            pool = ThreadPool(processes=1)

            async_result = pool.apply_async(self.spot_yt.parse_data, [url]) # tuple of args for foo

            # do some other stuff in the main process

            self.queue.setdefault(guildid, []).extend(async_result.get())

        elif any(plat in url for plat in platform_list) == True:
            logs.debug('it a url')
            self.queue.setdefault(guildid, []).append(url)

        else:
            if 'ytmusic' in platform:
                a = ytmusic.search(query=url,filter='songs',limit=1,ignore_spelling=True)
                if a:
                    pass
                else:
                    raise noVideoFound()
                vid = 'https://music.youtube.com/watch?v=' + a[0]['videoId']
                logs.debug(vid)
                self.queue.setdefault(guildid, []).append(vid)
            else:
                a = yt_search.main(url)
                if a == False:
                    raise noVideoFound()
                else:
                    self.queue.setdefault(guildid, []).append(a)

    def insert_song(self, guildid,url: str, platform='youtube'):
        platform_list = ['https://www.youtube.com', 'https://music.youtube.com/watch?v=']
        if "https://www.youtube.com/playlist?list=" in url:
            raise insertPlaylist()

        elif 'https://youtu.be/' in url:
            rename = url.replace('https://youtu.be/','')
            fullname = 'https://www.youtube.com/watch?v=' + rename
            self.queue.setdefault(guildid, []).insert(1, fullname)

        elif any(plat in url for plat in platform_list) == True:
            logs.debug('it a url')
            self.queue.setdefault(guildid, []).insert(1,url)

        elif 'https://music.youtube.com/playlist?list=OLAK5uy_' in url:
            logs.debug('it a youtube music alblum')
            idn = url.replace('https://music.youtube.com/playlist?list=','')
            a = ytmusic.get_album_browse_id(idn)
            b = ytmusic.get_album(a)
            for d in b['tracks']:
                x = d['videoId']
                f = 'https://music.youtube.com/watch?v=' + x
                self.queue.setdefault(guildid, []).insert(1,f)
        else:
            if 'ytmusic' in platform:
                a = ytmusic.search(query=url,filter='songs',limit=1,ignore_spelling=True)
                if a:
                    pass
                else:
                    raise noVideoFound()
                logs.debug(a)
                vid = 'https://music.youtube.com/watch?v=' + a[0]['videoId']
                logs.debug(vid)
                self.queue.setdefault(guildid, []).insert(1,vid)
            else:
                a = yt_search.main(url)
                if a == False:
                    raise noVideoFound()
                else:
                    self.queue.setdefault(guildid, []).insert(1,a)

    def get_song_data(self, guildid ,index=0):
        # print(self.queue.get(guildid))
        if self.queue.get(guildid) == None:
            logs.info('no guild found createing one ')
            self.queue.setdefault(guildid,[])
            if self.currentsong.get(guildid) == None:
                return None
        elif index == 0:
            print(self.currentsong.get(guildid))
            if self.currentsong.get(guildid) == None:
                return None
            else:
                songq = self.currentsong[guildid]
        else:
            songq = self.queue[guildid][index]

        videoinfo = yt_data.parse_data(songq)
        return videoinfo

    # def view_queue(self, guildid):
    #     to_be_process = []
    #     lp = 0
    #     finalstr = []
    #     loops = 0
    #     if len(self.queue[guildid]) == 0:
    #         return 'No Song in queue', None
    #     elif len(self.queue[guildid]) <= 6:
    #         loops = len(self.queue[guildid])
    #     elif len(self.queue[guildid]) >= 6:
    #         loops = 6
    #     for tobe in range(loops):
    #         to_be_process.append(self.queue[guildid][tobe])
    #     for la in to_be_process:
    #         data = yt_data.parse_data(la)
    #         name = data['videoname']

    def list_queue(self,guildid):
        n = 0
        j = 0
        buffer = []
        output = []
        if self.queue.get(guildid) == None:
            logs.info('no guild have been created')
            logs.info('creatinoneone')
            self.queue.setdefault(guildid, [])
            logs.info('created successfully')
            return 'No Song in queue' , None
        elif len(self.queue[guildid]) == 0:
            return 'No Song in queue' , None
        elif len(self.queue[guildid]) <= 6:
            n = len(self.queue[guildid])
        else:
            n = 6
        for n in range(n):
            logs.debug('list queue first loop is running')
            res = yt_data.parse_data(self.queue[guildid][n])
            logs.info(self.queue[guildid][n])
            buffer.append(res['videoname'])
            logs.info('queue second main loop had been run')
        cts = yt_data.parse_data(self.currentsong[guildid])
        for n, i in enumerate(buffer):
            if n == 0:
                p = 'Now playing ' + '[' + cts['videoname'] + ']' + '(' + self.currentsong[guildid] + ')'
                output.append(p)
            elif n >= 1:
                j += 1
                test = str(j) + ') ' + '[' + i + ']' + '(' + self.queue[guildid][n] + ')'
                output.append(test)
            convertstr = str(output)[1:-1]
            outa = convertstr.replace(',', '\n')
        if len(self.queue) < 5:
            return outa, True
        else:
            return outa, False

    def removelast(self, guildid):
        del self.queue.setdefault(guildid, [])[-1]

    def remove_song(self, guildid,index: int):
        removed_song = self.queue[guildid][index]
        song_nunber = self.queue.setdefault(guildid, []).index(removed_song)
        self.queue.setdefault(guildid, []).pop(index)
        data = yt_data.parse_data(removed_song)
        r_song = str(data['videoname']) + str(data['url'])
        return r_song, song_nunber

    def clearlist(self, guildid):
        try:
            del self.queue[guildid][:]
        except:
            pass

    def shuffle(self, guildid):
        random.shuffle(self.queue[guildid])

    def sauce(self, guildid):
        return self.currentsong[guildid]

    def set_current_song(self, guildid,url:str):
        self.currentsong[guildid] = url

    def progess_song(self, guildid):
        if self.isinfiteloop[guildid] == True :
            logs.info('playing new songs')
            self.queue.setdefault(guildid, []).pop(0)
            self.queue.setdefault(guildid, []).insert(1,self.currentsong[guildid])
        else:
            logs.debug('triming old history command')
            try:
                a = self.queue.setdefault(guildid, []).pop(0)
                self.history.setdefault(guildid, []).insert(0,a)
            except:
                pass

        try:
            if len(self.history[guildid]) >=2:
                self.history.setdefault(guildid, []).pop(-1)
        except:
            pass

    def get_history(self , guildid):
        return self.history[guildid][0]

    def beforeinfo(self, guildid):
        videoinfo = yt_data.parse_data(self.history[guildid][0])
        return videoinfo

