import asyncio
import random
from re import A

import discord
import yt_dlp
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext import bridge
from discord.ext.bridge import BridgeContext, BridgeExtContext,BridgeApplicationContext
from discord.utils import get

from ...log import logs

from ...fileio import botconfig
from .lib.main import musicss

# seting = open('config/botsetting.yaml')
# # # a = open('botsetting.yaml')
# botconfig = yaml.load(seting, Loader=yaml.FullLoader)


music = musicss()

autoleave = {}
vctimmer = {}
# coding:utf-8

_loop = asyncio.get_event_loop()


timeouttime = botconfig['bot_setting']['disconnecttime']
adminacc = list(botconfig['bot_setting']['botadminacc'])
hexcolour = int(botconfig['bot_setting']['colour'],16)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logs.info('music module online')
        for guild in self.client.guilds:
            guildid = str(guild.id)
            music.isinfiteloop[guildid] = False
            autoleave[guild.id] = False

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if after.channel == None:
        if after.channel == None and member.id == self.client.user.id: #replce this when torcher test fail
            voice = get(self.client.voice_clients, channel__guild__id = before.channel.guild.id)
            logs.debug('clearing playlist requirement meet')
            music.clearlist(guildid=str(before.channel.guild.id))
            if music.isinfiteloop.get(str(before.channel.guild.id)) == True:
                music.isinfiteloop[str(before.channel.guild.id)] = False
            return

        if member.id == self.client.user.id:
            return
        if before.channel != None:
            voice = get(self.client.voice_clients, channel__guild__id = before.channel.guild.id)
            if voice == None:
                return
            if voice.channel.id != before.channel.id:
                return
            if len(voice.channel.members) <= 1:
                if autoleave.get(before.channel.guild.id) == False:
                    vctimmer[before.channel.guild.id] = 0

                    while True:
                        logs.debug("time", str(vctimmer[before.channel.guild.id]))

                        await asyncio.sleep(1)

                        vctimmer[before.channel.guild.id] += 1

                        if len(voice.channel.members) >= 2:
                            vctimmer[before.channel.guild.id] = 0
                            return
                        if vctimmer[before.channel.guild.id] >= int(timeouttime):
                            await voice.disconnect()
                            vctimmer[before.channel.guild.id] = 0
                            music.clearlist(guildid=str(before.channel.guild.id))
                            if music.isinfiteloop.get(str(before.channel.guild.id)) == True:
                                music.isinfiteloop[str(before.channel.guild.id)] = False
                            return

    @bridge.bridge_command(aliases=['come', 'cum'])
    # @bridge.bridge_command(aliases=['come', 'cum'])
    async def join(self, ctx):
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()

    @bridge.bridge_command(aliases=['fuckoff'])
    async def leave(self, ctx):
        guildid = str(ctx.guild.id)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            if ctx.invoked_with == 'fuckoff':
                await ctx.send(random.choice(botconfig['bot_reply']['leavef']))
            else:
                await ctx.send(random.choice(botconfig['bot_reply']['leave2']))
        else:
            if ctx.invoked_with == 'fuckoff':
                await ctx.send(random.choice(botconfig['bot_reply']['leavef']))
            else:
                await ctx.send(random.choice(botconfig['bot_reply']['leave']))
        await ctx.guild.voice_client.disconnect()
        music.clearlist(guildid=guildid)
        if music.isinfiteloop.get(guildid) == True:
            music.isinfiteloop[guildid] = False

    @bridge.bridge_command(aliases=['p'])
    async def play(self, ctx, *, url= None):
        await self.join(ctx)
        guildid = str(ctx.guild.id)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if url == None:
            await ctx.send('are we suppose to be playing something here?')
        else:
            a = music.add_song(guildid=guildid,url=url)
            if a != None:
                await ctx.send(a)
            else:
                if not voice.is_playing():
                    self.player(guildid=guildid,ctx=ctx)
                else:
                    await ctx.send('this song had been added to the queue')

    @bridge.bridge_command(aliases=['pnext'])
    async def playnext(self, ctx, *, url = None):
        await self.join(ctx)
        guildid = str(ctx.guild.id)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if url == None:
            await ctx.send('are we suppose to be playing something here?')
        else:
            a = music.insert_song(guildid=guildid, url=url)
            if a != None:
                await ctx.send(a)
            else:
                if not voice.is_playing():
                    self.player(guildid=guildid,ctx=ctx)
                else:
                    await ctx.send('Ok this song will be play next')

    @bridge.bridge_command(aliases=['pnow'])
    async def playnow(self, ctx, *, url= None):
        await self.join(ctx)
        guildid = str(ctx.guild.id)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if url == None:
            await ctx.send('are we suppose to be playing something here?')
        else:
            a = music.insert_song(guildid=guildid,url=url)
            if a != None :
                await ctx.send(a)
            else:
                if not voice.is_playing():
                    self.player(guildid=guildid,ctx=ctx)
                else:
                    voice.stop()
                    voice.is_playing()
                    self.player(guildid,ctx, ignore=True)

    @bridge.bridge_command()
    async def ytmusic(self, ctx, * ,url = None):
        await self.join(ctx)
        guildid = str(ctx.guild.id)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if url == None:
            await ctx.send('are we suppose to be playing something here?')
        else:
            a = music.add_song(guildid=guildid,url=url,platform='ytmusic')
            if a != None:
                await ctx.send(a)
            else:
                if not voice.is_playing():
                    self.player(guildid=guildid,ctx=ctx)
                else:
                    await ctx.send('Ok this song had been added to the queue')

    @bridge.bridge_command(aliases=['current','song','currentsonginfo'])
    async def info(self, ctx, index=0):
        guildid = str(ctx.guild.id)
        song = music.get_song_data(index=index,guildid=guildid)
        if index == 0:
            await ctx.send(f'''song in queue number {index}
the current song playing is: {song['videoname']}
...and it has been viewed {song['view']} times!
also here's the link! --> {song["url"]}
which have {song["like"]} like
... and a {song["dislike"]}''')
        else:
            await ctx.send(f'''song in queue number {index}
{song['videoname']}
...and it has been viewed {song['view']} times!
also here's the link! --> {song["url"]}
which have {song["like"]} like
... and a {song["dislike"]}''')

    @bridge.bridge_command()
    async def beforeinfo(self, ctx):
        guildid = str(ctx.guild.id)
        song = music.beforeinfo(guildid=guildid)
        await ctx.send(f'''the song that just played is {song['videoname']}
...and it has been viewed {song['view']} times!
also here's the link! --> {song["url"]}
which have {song["like"]} like
... and a {song["dislike"]}''')

    @bridge.bridge_command(aliases=['is24/7'])
    async def isafk(self, ctx):
        guildid = ctx.guild.id
        if autoleave.get(guildid) == True:
            await ctx.send('24/7 is enable')
        else:
            await ctx.send('24/7 is disable')

    @bridge.bridge_command(aliases=['24/7'])
    async def toggleafk(self, ctx):
        guildid = ctx.guild.id
        userid = ctx.author.id
        if userid in adminacc:
            if autoleave.get(guildid) == False:
                autoleave[guildid] = True
                await ctx.send('Ok I will be standby in this vc 24/7')
                return
            if autoleave.get(guildid) == True:
                autoleave[guildid] = False
                await ctx.send('Ok I will not afk here')
                return
        else:
            await ctx.send('you aint my dad fam')

    @bridge.bridge_command(aliases=['clear'])
    async def clearlist(self, ctx):
        music.clearlist(guildid=str(ctx.guild.id))
        await ctx.send('gotchu, list cleared!')

    @bridge.bridge_command()
    async def queue(self, ctx):
        msg, a = music.list_queue(guildid=str(ctx.guild.id))
        embeds = discord.Embed(title='Song in queue', description=msg ,type='link', color=hexcolour)
        if a == True:
            embeds.add_field(name='and more playing', value='\u200b')
        elif a == False:
            pass
        else:
            await ctx.send('No song in queue')
            return
        await ctx.send(embed=embeds)

    @bridge.bridge_command()
    async def shuffle(self, ctx):
        music.shuffle(guildid=str(ctx.guild.id))
        await ctx.send(random.choice(botconfig['bot_reply']['shuffle']))

    @bridge.bridge_command()
    async def lremove(self, ctx):
        music.removelast(guildid=str(ctx.guild.id))
        await ctx.send('Ok, removed last song in queue')

    @bridge.bridge_command(pass_context=True)
    async def remove(self, ctx, songnum=None):
        if songnum == None:
            await ctx.send('give me the song number to be remove from queue')
            await self.queue(ctx)
        else:
            songnuma = int(songnum)
            a, b = music.remove_song(guildid=str(ctx.guild.id),index=songnuma)
            embeds = discord.Embed(title=f'Ok removed song number {b}', description=a ,type='link', color=hexcolour)
            await ctx.send(embed=embeds)

    @bridge.bridge_command(aliases=['sauce'])
    async def warp(self, ctx):
        await ctx.send(music.sauce(guildid=str(ctx.guild.id)))

    @bridge.bridge_command(aliases=['next','kingcrimson!','foward'])
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.send(random.choice(botconfig['bot_reply']['skip']))

    @bridge.bridge_command()
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.resume()
            await ctx.send(random.choice(botconfig['bot_reply']['resume']))

    @bridge.bridge_command()
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send(random.choice(botconfig['bot_reply']['pause']))

    @bridge.bridge_command(aliases=['songcount', 'total'])
    async def count(self, ctx):
        guildid = str(ctx.guild.id)
        await ctx.send("counting...")
        await ctx.send(f" {len(music.queue[guildid])} songs are in this queue")

    @bridge.bridge_command()
    async def seek(self, ctx, timestamp=None):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        guildid = str(ctx.guild.id)
        if timestamp == None:
            await ctx.send('give me the time to seek the play head too')
        else:
            music.queue.setdefault(guildid, []).insert(1,music.currentsong[guildid])
            voice.stop()
            voice.is_playing()
            logs.info(f'seeking play head to {timestamp}')
            self.player(guildid,ctx,timestamp, ignore=True)
            await ctx.send(f'skiped to {timestamp}')

    @bridge.bridge_command(aliases=['bitethedust!','backward','previous'])
    async def again(self, ctx):
        guildid = str(ctx.guild.id)
        music.queue.setdefault(guildid, []).insert(1,music.history[guildid][0])
        await ctx.send('Ok that song will be play again next')

    @bridge.bridge_command()
    async def addbefore (self, ctx):
        guildid = str(ctx.guild.id)
        music.queue.setdefault(guildid, []).append(music.history[guildid][0])
        await ctx.send("The previous song has now added to the queue!")

    @bridge.bridge_command(aliases=['looplist'])
    async def loopplaylist(self, ctx, a=None):
        if a == None:
            await ctx.send('give me ammount of time to loop the playlist')
        elif int(a) <= 1000:
            guildid = str(ctx.guild.id)
            adda = music.queue[guildid]
            for n in range(int(a)):
                music.queue.setdefault(guildid, []).extend(adda)
                logs.info(f"looped playlist {n} times")
            await ctx.send(f"Alright, the entire playlist will be looped {a} times!")
            del adda
        else:
            await ctx.send('Give me something say less that a 1000')

    @bridge.bridge_command()
    async def loop(self, ctx, a=None):
        guildid = str(ctx.guild.id)
        logs.debug('i have been run')
        if a == None:
            logs.debug('ok at lease ')
            logs.debug(music.isinfiteloop[guildid])
            if music.isinfiteloop.get(guildid) == True:
                music.isinfiteloop[guildid] = False
                await ctx.send('ok I had stopped the loop')
                return
            if music.isinfiteloop.get(guildid) == False:
                music.isinfiteloop[guildid] = True
                await ctx.send('ok looping this song infinitely')
                return

        elif int(a) <= 1000:
            for n in range(int(a)):
                music.queue.setdefault(guildid, []).append(music.currentsong[guildid])
                logs.info(f"looped song {n} times")
            await ctx.send(f"Alright, this song will be looped {a} times!")
        else:
            await ctx.send("Give me something say less than 1000")

    @bridge.bridge_command(aliases=['isloop'])
    async def isitloop(self, ctx):
        guildid = str(ctx.guild.id)
        if music.isinfiteloop.get(guildid) == True:
            await ctx.send('I am in an loop')
        if music.isinfiteloop.get(guildid) == False:
            await ctx.send('I am not in a loop')

    @bridge.bridge_command()
    async def playpooh(self, ctx):
        guildid = str(ctx.guild.id)
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()
        url = ['https://www.youtube.com/playlist?list=PLKu0PlxNFnZUjUzSxccTzHOgEYYGlSJk5',
               'https://music.youtube.com/playlist?list=OLAK5uy_kIa_eK4TM_gMkf44jFK118aDSnxYSgVxI']
        music.clearlist(guildid=guildid)
        respond = ['Playing father playlist','daddy favorite playlist music','Ok good pick I see you have a shit taste here']
        for a in url:
            music.add_song(guildid=guildid,url=a)
        music.shuffle(guildid=guildid)
        self.player(guildid=guildid,ctx=ctx)
        await ctx.send(random.choice(respond))

    @bridge.bridge_command()
    async def playjag(self, ctx):
        guildid = str(ctx.guild.id)
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()
        music.clearlist(guildid=guildid)
        respond = ['Playing jag playlist on spotify \n might take a while to start since i have to convert spotify link to yotube']
        music.add_song(guildid=guildid,url='https://open.spotify.com/playlist/37i9dQZF1EprefcXJEAqWX?si=1713c2c44b384d72')
        music.shuffle(guildid=guildid)
        self.player(guildid=guildid,ctx=ctx)
        await ctx.send(random.choice(respond))

    @bridge.bridge_command()
    async def playitchys(self, ctx):
        guildid = str(ctx.guild.id)
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()
        music.clearlist(guildid=guildid)
        respond = ['Playing father playlist','daddy favorite playlist music','Ok good pick I see you have a shit taste here']
        music.add_song(guildid=guildid,url='https://www.youtube.com/playlist?list=PLSJh9S2IPebGSSqkXACtbCJJcYc26Iy3i')
        music.shuffle(guildid=guildid)
        self.player(guildid=guildid,ctx=ctx)
        await ctx.send(random.choice(respond))

    @bridge.bridge_command()
    async def playitchy2019 (self,ctx):
        guildid = str(ctx.guild.id)
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()
        url = [ 'https://www.youtube.com/playlist?list=PLQJHbSBLRWJQS-q5yFzhxo3ibjFYREuvI',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJTPyj6wUe72-UdJEBEcQW2_',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJQfxi0ry3VnnioDvOCfODgF',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJRpoPK3MMtNy2JkxhbjRAE3',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJQZo3ab7BEZW4gDWyaSKmWn',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJR4AHkFx4sK8QKU5lWBiioU',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJRX8mSWWwtLgSVy5sf_2GnH']
        music.clearlist(guildid=guildid)
        respond = ["Playing itchy’s act 1!", "wow, a classic!", "itchy's first playlist huh?\ngotchu!"]
        for i in url:
            music.add_song(guildid=guildid,url=i)
        music.shuffle(guildid=guildid)
        self.player(guildid=guildid,ctx=ctx)
        await ctx.send(random.choice(respond))

    @bridge.bridge_command()
    async def playitchy2020 (self,ctx):
        guildid = str(ctx.guild.id)
        channels = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channels)
        else:
            voice = await channels.connect()
        url = ['https://www.youtube.com/playlist?list=PLQJHbSBLRWJSPZjTDPaIaLXpM7-JMI7RG',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJQuWq0QTB02dcemPwQlMUTJ',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJSV2Ocjftmp1ekoIXBFjXTs',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJT5mm_k0kfgzF0jEBaJOGAK',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJR75XSSvSSv7SlA6BY-ZZsd',
            'https://www.youtube.com/playlist?list=PLQJHbSBLRWJRyfU8N23zI59rq-FaGGQOW',
            'https://youtube.com/playlist?list=PLQJHbSBLRWJQgrteRNu9e6317iTUcSCUh']
        music.clearlist(guildid=guildid)
        respond = ["Playing itchy’s act 2!", "Ooo, my favorite!", "itchy's playlist huh?\ngotchu!"]
        for i in url:
            music.add_song(guildid=guildid,url=i)
        music.shuffle(guildid=guildid)
        self.player(guildid=guildid,ctx=ctx)
        await ctx.send(random.choice(respond))

    def player(self , guildid, ctx, timestamp='00:00',ignore=False):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ', 'options': f'-vn -ss {timestamp}'}
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_playing() and ignore == False:
            guildid = str(ctx.guild.id)
            if music.queue[guildid]:
                a = music.queue[guildid][0]
                music.set_current_song(url=a,guildid=guildid)
                try:
                    
                    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(a, download=False)

                    URL = info['url']
                    voice.play(FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
                    voice.is_playing()
                    logs.debug('playing')
                except:
                    logs.info('video error')
                    asyncio.run_coroutine_threadsafe(self.sendthing(guildid=guildid, ctx=ctx,message='video error'), _loop)
            else:
                logs.info('no more music in playlist')
                asyncio.run_coroutine_threadsafe(self.sendthing(guildid=guildid, ctx=ctx,message='empty list'), _loop)
        else:
            logs.debug('seek or insert function in use')

    def play_next(self,ctx):
        guildid = str(ctx.guild.id)
        music.progess_song(guildid=guildid)
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if not voice.is_playing():
                self.player(ctx=ctx,guildid=guildid)
        except AttributeError:
            pass

    async def sendthing(self, guildid, ctx, message:str):
        if message in 'video error':
            await ctx.send('This video is not accessable or age restriceted. Please check if the video is publicly accessable without account')
            asyncio.run_coroutine_threadsafe(self.play_next(ctx), _loop)
            return
        elif message in 'empty list':
            await ctx.send('No more music in the playlist')
            return
        elif message in 'disconnected':
            await ctx.send('Geez just ask me to leave nicely and i will do so ok')
            music.clearlist(guildid=guildid)
            if music.isinfiteloop.get(guildid) == True:
                music.isinfiteloop[guildid] = False
            return


def setup(client):
    client.add_cog(Music(client))
