import random

from ytmusicapi import YTMusic

from . import spot_yt, yt_data, yt_playlist, yt_search

# coding:utf-8
from ....log import logs

ytmusic = YTMusic()

class musicss:

    def __init__(self):
        self.queue = {}
        self.history = {}
        self.isinfiteloop = {}
        self.currentsong = {}

    def add_song(self, guildid ,url: str, platform='youtube'):
        platform_list = ['https://www.youtube.com', 'https://music.youtube.com/watch?v=']
        if "https://www.youtube.com/playlist?list=" in url:
            self.queue.setdefault(guildid, []).extend(yt_playlist.parse_data(url))
            del yt_playlist.playlist[:]
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
            self.queue.setdefault(guildid, []).extend(spot_yt.parse_data(url))

        elif any(plat in url for plat in platform_list) == True:
            logs.debug('it a url')
            self.queue.setdefault(guildid, []).append(url)

        else:
            if 'ytmusic' in platform:
                a = ytmusic.search(query=url,filter='songs',limit=1,ignore_spelling=True)
                if a:
                    pass
                else:
                    raise Exception('music not found')
                vid = 'https://music.youtube.com/watch?v=' + a[0]['videoId']
                logs.debug(vid)
                self.queue.setdefault(guildid, []).append(vid)
            else:
                a = yt_search.main(url)
                if a == False:
                    raise Exception('video not found')
                else:
                    self.queue.setdefault(guildid, []).append(a)

    def insert_song(self, guildid,url: str, platform='youtube'):
        platform_list = ['https://www.youtube.com', 'https://music.youtube.com/watch?v=']
        if "https://www.youtube.com/playlist?list=" in url:
            raise Exception('inserting playlist is not allow')

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
                    raise Exception('No music found')
                logs.debug(a)
                vid = 'https://music.youtube.com/watch?v=' + a[0]['videoId']
                logs.debug(vid)
                self.queue.setdefault(guildid, []).insert(1,vid)
            else:
                a = yt_search.main(url)
                if a == False:
                    raise Exception("No music Found")
                else:
                    self.queue.setdefault(guildid, []).insert(1,a)

    def get_song_data(self, guildid ,index=0):
        if index == 0:
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
        # if self.queue[guildid] not in self.queue:
        #     raise Exception('no song yet')
        if len(self.queue[guildid]) == 0:
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

