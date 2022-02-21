from __future__ import unicode_literals
import logging
import time
import pathlib
import os
from pydoc import cli
from tempfile import TemporaryFile
from discord import embeds
from discord.ext.commands.errors import CommandError
from discord.ext import tasks
import yt_dlp
from token import EQUAL, LESSEQUAL
import asyncio
#python music bot.py
from youtubesearchpython import *
from youtubesearchpython.__future__ import VideosSearch
import discord
from discord.ext import commands    
# from discord.ext import CommandError
from discord.utils import get
from discord import FFmpegPCMAudio
import configparser
from youtubesearchpython import Search
from youtubesearchpython.__future__.search import ChannelsSearch
import random
import time
import scrapetube
_loop = asyncio.get_event_loop()
# coding:utf-8
config_string =  'config/config.ini'
abspath = os.path.abspath(config_string)
config =  configparser.ConfigParser()
# print(abspath)
config.read(abspath)
config.sections()

client = discord.Client()
# print(config['botsetting']['bot_token'])
client = commands.Bot(command_prefix=config['botsetting']['bot_prefix'])  # prefix our commands with '.'
# slashclient = discord.Bot()
client.remove_command("help")
timeouttime = config.getint('botsetting','timeouttime')
admin_account =  config.getint('botsetting','admin_account')

imagedirpath = 'config/profile/'

autoleave = {}

isloop = {}

play_que = {}
hadplay = {}
backinfo = {}
vctimmer = {}

disconnected_time = {}

reactui = {}

updatecurrentsong = {}

spammerlist = {}

#respond list for itchy 
reply = ['alright, see you soon!',"oh no, it's time to go?","utachi...\nout!"]
replybfr = ['owh please let me play a few hundred songs before i go—', "what why— that song was great!","what why— things were getting good!","hey! i am not finished yet!"]
replyf = ["meanie beanie!\n.·´¯`(>▂<)´¯`·. ","imma go cry in my digital corner (┬┬﹏┬┬)","GRrrrrr, that's it!\n💨","i have robotic feelings you know!","red Fine!","what an angry baby you are!"]
shuffleres = ['Okay, shuffling the queue...','shaking it up!','order is now nonexistent.','RNG time baby~']
replyskip = ["yup let's!",'finally!','Hey, we were at the good part!','b-but that song was nice…','song skipped!','sure can do!','KING CRIMSON']
replypause = ['ZA WARUDO!','Okay!','am i too loud for you?','music break?','stopped.']

#ICHIRO ICHIRO ICHIRO, THIS IS AN EXAMPLE FOR MAKING A RANDOM CHOICE RESPONSE AND SHIT
#@client.command()
# async def leave(ctx):
#     channels = ctx.message.author.voice.channel
#     voice = get(client.voice_clients, guild=ctx.guild)    
#     if voice.is_connected():
#         if voice.is_playing():
#             await ctx.reply(random.choice(VARIABLE)) <------------- IMPORTANT TO MAKE RANDOM REPLIES.
#             await ctx.guild.voice_client.disconnect()
#             await ctx.send('``>Bot left``')
#             guildid = ctx.message.guild.id


#if you don't know what you are doing don't touch the code below


# check if bot is ready
@client.event  
async def on_ready():
    for guild in client.guilds:
        print('you ok bro')
        guildid = guild.id
        isloop[guildid] = False
        autoleave[guildid] = False
        reactui[guildid] = False
        updatecurrentsong[guildid] = False
    print('Bot online')

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel == None:            
        print('trying to clear playlist ok')
        guildid = before.channel.guild.id
        disconnected_time[guildid] = 0
        while True:

            disconnected_time[guildid] +=1

            await asyncio.sleep(1)
            if disconnected_time[guildid] >= 60:
                del play_que.setdefault(guildid, [])[:]
                if isloop.get(before.channel.guild.id):
                    isloop[before.channel.guild.id] = False
                disconnected_time[guildid] == 0
                return
            
    if member.id == client.user.id:
        return
    if before.channel != None:
        voice = get(client.voice_clients, channel__guild__id = before.channel.guild.id)
        if voice == None:
            return
        if voice.channel.id != before.channel.id:
            return
        if len(voice.channel.members) <= 1:
            if autoleave.get(before.channel.guild.id) == False:
                vctimmer[before.channel.guild.id] = 0
                
                while True:
                    print("time", str(vctimmer[before.channel.guild.id]))

                    await asyncio.sleep(60)
                    
                    vctimmer[before.channel.guild.id] += 1

                    if len(voice.channel.members) >= 2:
                        vctimmer[before.channel.guild.id] = 0
                        break
                    if vctimmer[before.channel.guild.id] >= int(timeouttime):
                        await voice.disconnect()
                        del play_que.setdefault(before.channel.guild.id, [])[:]
                        if isloop.get(before.channel.guild.id) == True:
                            isloop[guildid] = False
                        break
    

@client.command(aliases=['is24/7'])
###ANTI#SPAM##
async def checka(ctx):
    guildid = ctx.message.guild.id
    if autoleave.get(guildid) == False:
        await ctx.send('24/7 is enable')
    else:
        await ctx.send('24/7 is disable')

@client.command(aliases=['24/7'])
###ANTI#SPAM##
async def toggleon(ctx):
    userid = ctx.message.author.id
    # print(userid)
    # print(admin_account)
    # print(hex(userid))
    # print(hex(int(admin_account)))
    if int(admin_account) == userid:
        guildid = ctx.message.guild.id
        if autoleave.get(guildid) == False:
            autoleave[guildid] = True
            await ctx.send('Ok I will be standby in this vc 24/7')
            return
        if autoleave.get(guildid) == True:
            autoleave[guildid] = False
            await ctx.send('Ok I will not afk here')
            return
    if userid != int(admin_account):
        await ctx.send('you are not the one who gave me life i aint following your command')


# command for bot to join the channels of the user, if the bot has already joined and is in a different channels, it will move to the channels the user is in
@client.command(aliases=['come', 'cum'])
###ANTI#SPAM##
async def join(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()


# leave command
@client.command()
###ANTI#SPAM##
async def leave(ctx):
    guildid = ctx.message.guild.id
    voice = get(client.voice_clients, guild=ctx.guild)    
    if voice.is_playing():
        await ctx.reply(random.choice(replybfr))
        await ctx.guild.voice_client.disconnect()
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
        if isloop.get(guildid):
            isloop.pop(guildid)
    else:
        await ctx.reply(random.choice(reply))
        await ctx.guild.voice_client.disconnect()
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
        if isloop.get(guildid):
            isloop.pop(guildid)

# rude leave
@client.command()
###ANTI#SPAM##
async def fuckoff(ctx):
    guildid = ctx.message.guild.id
    voice = get(client.voice_clients, guild=ctx.guild)    
    if voice.is_connected():
        await ctx.reply(random.choice(replyf))
        await ctx.guild.voice_client.disconnect() # Leave the channels
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
        if isloop.get(guildid) == True:
            isloop[guildid] == False

    else:
        await ctx.reply(random.choice(replyf))
        await ctx.guild.voice_client.disconnect() # Leave the channels
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
        if isloop.get(guildid) == True:
            isloop[guildid] == False

# manunal command
@client.command(aliases=['help','manunal'])
###ANTI#SPAM##
async def man(ctx):
    embeds = discord.Embed(title='Manunal', description='-play insert search terms or url or playlist link (support playing from youtube and youtube music) \n if the video is the part of the playlist I will only play the song and not the whole playlist \n -playnext simlar to play but this will insert the song to be play after the current song \n -playnow is the same as playnext but will play the song instantly \n -queue will show the song in queue \n -info is to get the current song playing info add an number to get the song info in queue at postion \n -clearlist is to clear the playlist \n -join is to join the vc \n -leave is to leave the vc \n -skip is for skipping the song \n -pause is to pause the music \n -resume is to resume the music \n -shuffle is to shuffle the song in playlist \n -lremove is to remove the last song in the queue \n -count is to count the total song in queue \n -seek is to seek to the timestamp in song \n -beforeinfo is to get the info of the song that just play before \n -again is the add the song that just play to be play next after the current song is done playling \n -addbefore is the add the song that just done playing to the last postion of the queue in the playlist \n -loop is to loop the current song \n -loopplaylist is to loop the current song in queue \n -warp is to get the song url \n -is24/7 to see if i will be afk in a vc \n -remove is to remove the song number in queue \n -isloop check if bot is in a infite loop \n [full github manunal here](https://github.com/poohzaza166/Utachi-discord/wiki)', color=0xfff347)
    await ctx.send(embed=embeds)

# abit of easter egg
@client.command()
###ANTI#SPAM##
async def groovy(ctx, *, a):
    
        
    await ctx.send('wrong person he not here')

# shuffle command
@client.command()
###ANTI#SPAM##
async def shuffle(ctx):
    guildid = ctx.message.guild.id
    random.shuffle(play_que.setdefault(guildid, []))
    
        
    await ctx.send(random.choice(shuffleres))

# clear playlist command 
@client.command(aliases=['clear'])
###ANTI#SPAM##
async def clearlist(ctx):
    clearlistres = ["gotchu, list cleared!"]# edit shit here
    guildid = ctx.message.guild.id
    del play_que.setdefault(guildid, [])[:]
    
        
    await ctx.send(random.choice(clearlistres))

# remove the last song from playlist
@client.command()
###ANTI#SPAM##
async def lremove(ctx):
    bremoveres = ["gotchu, I have removed the last song!"]
    guildid = ctx.message.guild.id
    del play_que.setdefault(guildid, [])[-1]
    
        
    await ctx.send(random.choice(bremoveres))

# check the song in queue
@client.command()
###ANTI#SPAM##
async def queue(ctx):
        guildid = ctx.message.guild.id
        j = 0
        now_playing = play_que.get(guildid)
        listofplay = []
        actual2 = []
        if len(now_playing) == 0:
            await ctx.send("no song in queue")
            return
        elif len(now_playing) < 6:
            ammountoftime = len(now_playing)
        else:
            ammountoftime = 6
        print(now_playing[0])
        for n in range(ammountoftime):
            video = Video.get(now_playing[n])
            listofplay.append(video['title'])
        currnetsong =  Video.getInfo(playurl, mode= ResultMode.json)
        s = currnetsong['title']
        for a, i in enumerate(listofplay):
            print(a)
            print(i)
            if a == 0:
                lol = 'Now playing ' + '[' + s + ']' + '(' + playurl + ')'
                actual2.append(lol)
            elif a >= 1:
                j += 1
                test = str(j) + ') ' + '[' + i + ']' + '(' + now_playing[a] + ')'
                actual2.append(test)
        print(actual2)
        convertstring = str(actual2)[1:-1]
        actuallist = convertstring 
        list1 = actuallist.replace(',', '\n\n' )
        embeds = discord.Embed(title='Song in queue', description=list1 ,type='link', color=0xfff347)
        if len(now_playing) < 5:
            await ctx.send(embed=embeds)
        else:
            embeds.add_field(name='and more playing', value='\u200b')
            await ctx.send(embed=embeds)

@client.command()
###ANTI#SPAM##
async def remove(ctx, numbera=None):
    guildid = ctx.message.guild.id
    if numbera == None:
        await ctx.send('give me a song number to remove from queue')
        await queue(ctx)
    else:
        number = int(numbera)
        removed_song = play_que[guildid][number]
        song_number = play_que.setdefault(guildid, []).index(removed_song)
        play_que.setdefault(guildid, []).pop(number)
        videoinfo = Video.getInfo(removed_song, mode= ResultMode.json)
        # print(videoinfo)
        r_song = '[' + videoinfo['title'] + ']' + '(' + removed_song + ')'   
        embeds = discord.Embed(title=f'Ok removed song number {song_number}', description=r_song ,type='link', color=0xfff347)
        await ctx.send(embed=embeds)


# command to play sound from a youtube URL
@client.command(pass_context=True,aliases=['p'])
###ANTI#SPAM##
async def play(ctx, *, url=None):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)
    if url == None:
        await ctx.send('um \n were we suppose to be playing something here?')    
    elif "https://www.youtube.com/playlist?list=" in url:
        playlistid = url.replace("https://www.youtube.com/playlist?list=", '')
        videos = scrapetube.get_playlist(playlistid)
        for video in videos:
            videourl = "https://www.youtube.com/watch?v=" + video['videoId']
            play_que.setdefault(guildid, []).append(videourl)
        # while playlist:
        #     print('Getting more videos...')
        #     play_que.get(playlist.getVideos())
        print('ok')
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send("gotchu, playlist is now playing!")
        else:
                       
            await ctx.send('alright this playlist will be play next ')

    elif "https://www.youtube" or 'https://music.youtube' in url:
        print('it a url')
        play_que.setdefault(guildid, []).append(url)
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
                       
            await ctx.send ("alright this video will be play next")

    elif 'https://' in url:
        await ctx.send('it not a youtubelink')

    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).append(videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
                       
            await ctx.send('alright this video will be play next')

# command to play sound from a youtube URL next 
@client.command(pass_context=True,aliases=['pnext'])
###ANTI#SPAM##
async def playnext(ctx, *, url=None):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)
    if url == None:
        await ctx.send('um \n were we suppose to be playing something here?')        
    elif "https://www.youtube.com/playlist?list=" in url:      
        await ctx.send('adding playlist as a insert song is not supported')

    elif "https://www.youtube" or 'https://music.youtube' in url:
        print('it a url')
        play_que.setdefault(guildid, []).insert(1,url)
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
                       
            await ctx.send ("alright this video will be play next")

    elif 'https://' in url:
        await ctx.send('it not a youtubelink')

    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).insert(1,videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
                       
            await ctx.send('alright this video will be play next')

# command to play sound from a youtube URL now
@client.command(pass_context=True,aliases=['pnow'])
###ANTI#SPAM##
async def playnow(ctx, *, url=None):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)
    if url == None:
        await ctx.send('um \n were we suppose to be playing something here?')        
    elif "https://www.youtube.com/playlist?list=" in url:
        await ctx.send('adding playlist as a insert song is not supported')

    elif "https://www.youtube" or 'https://music.youtube' in url:
        print('it a url')
        play_que.setdefault(guildid, []).insert(1,url)
        if not voice.is_playing():
            startplay(ctx)
                       
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
            voice.stop()
                       
            await ctx.send ("alright this video will be play now")

    elif 'https://' in url:
        await ctx.send('it not a youtubelink')

    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).insert(1,videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)

            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
            voice.stop()
                       
            await ctx.send('alright this video will be play now')


# get the song url 
@client.command(aliases=['sauce'])
###ANTI#SPAM##
async def warp(ctx):
    guildid = ctx.message.guild.id
    print(playurl)      
    await ctx.send("the current song link playing is " + playurl)


# skip the song in playlist
@client.command(aliases=['next','kingcrimson!','foward'])
###ANTI#SPAM##
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()         
        await ctx.send(random.choice(replyskip))
        # play_next(ctx)


# command to resume voice if it is paused
@client.command()
###ANTI#SPAM##
async def resume(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
               
        await ctx.send('the music is resuming!')


# command to pause voice if it is playing
@client.command(aliases=['stop'])
###ANTI#SPAM##
async def pause(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
               
        await ctx.send(random.choice(replypause))

# give the current song info 
@client.command(aliases=['current','song','info'])
###ANTI#SPAM##
async def currentsonginfo(ctx, song=0, isplayed=False, nextsonginfo=None):
    guildid = ctx.message.guild.id
    if song == 0:
        songq = playurl
    else:
        songq = play_que[guildid][song]
    if isplayed == False:
        videoinfo = Video.getInfo(songq, mode= ResultMode.json)
               
        await ctx.send(f'song in queue number {song}')
        await ctx.send("the current song playing is: " + videoinfo['title'])
        await ctx.send("...and it has been viewed " + videoinfo['viewCount']['text'] + " times!")
        await ctx.send ("also here's the link! --> " + songq)
    else:
        if updatecurrentsong.get(guildid) == True:
            videoinfo = Video.getInfo(nextsonginfo, mode= ResultMode.json)
            list1 =  'Now playing ' + videoinfo['title'] 
            embeds = discord.Embed(title=list1 ,type='rich' ,url=nextsonginfo,color=0xfff347)
            # print(videoinfo['thumbnails'][0][0]['url'])
            embeds.set_image(url=videoinfo['thumbnails'][3]['url'])
            message = await ctx.send(embed=embeds)
        if reactui.get(guildid) == True:
            await message.add_reaction("⏪")
            await message.add_reaction("⏸️")
            await message.add_reaction("▶️")
            await message.add_reaction("⏭️")
            await message.add_reaction("🔁")
            global reactid
            reactid = str(message.id)
            print(reactid)
        

# debug command 
@client.command()
async def view(ctx):
    print(play_que)
    print("------------------------------------")
    print(hadplay)
    print("------------------------------------")
    print(backinfo)
    print("------------------------------------")
    print(autoleave)
    print("------------------------------------")
    print(isloop)
    print('------------------------------------')
    print(updatecurrentsong)

# count the current song in playlist
@client.command(aliases=['songcount', 'total'])
###ANTI#SPAM##
async def count(ctx):
    guildid = ctx.message.guild.id
    await ctx.send("counting...")       
    await ctx.send(f" {len(play_que[guildid])} songs are in this queue")

# the main play function
def startplay(ctx, timestamp='00:00'):
    guildid = ctx.message.guild.id
    print("started")
    if play_que[guildid]:
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ', 'options': f'-vn -ss {timestamp}'}
        voice = get(client.voice_clients, guild=ctx.guild)
        global playurl
        playurl = play_que[guildid][0]
        hadplay.setdefault(guildid, []).insert(0, playurl)
        if not voice.is_playing():
            try:
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(playurl, download=False)
                URL = info['url']
                voice.play(FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))   
                voice.is_playing()
                print('playing')
                # backinfo.setdefault(guildid, []).pop(0)
            except:
                # video_error(ctx)
                asyncio.run_coroutine_threadsafe(video_error(ctx), _loop)
    else:
        asyncio.run_coroutine_threadsafe(suck(ctx, a=False), _loop)

#function       
async def suck(ctx, a=False):

    if a == False:
        await ctx.send('no more music in playlist')
    else:
        await ctx.send('bot leave due to inactvity and clear music in the playlist')

async def video_error(ctx):
    await ctx.send('this video is not accessable or age restriceted please check if the video is publicly accessable without account')
    asyncio.run_coroutine_threadsafe(play_next(ctx), _loop)


# skip to parts in song 
@client.command()
###ANTI#SPAM##
async def seek(ctx, timestamp=None):
    voice = get(client.voice_clients, guild=ctx.guild)
    guildid = ctx.message.guild.id
    if timestamp == None:
        await ctx.send('give me the time to seek the play head too')
    else:        
        play_que.setdefault(guildid, []).insert(0,play_que[guildid][0])
        voice.stop()
        print(timestamp)
        startplay(ctx,timestamp)
        print(voice.is_playing())
        a = len(hadplay[guildid])
        if a >= 2:
            hadplay.setdefault(guildid, []).pop(2)
            await ctx.send(f'skiped to {timestamp}')   
        else:
            pass

# function
def play_next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    guildid = ctx.message.guild.id
    # time.sleep(5)
    if len(play_que[guildid]) >= 1:
        play_que.setdefault(guildid, []).pop(0)
    else:
        asyncio.run_coroutine_threadsafe(suck(ctx), _loop)
    if not guildid in backinfo:
        backinfo.setdefault(guildid, []).append(playurl)
    elif playurl != backinfo[guildid][-1]:
        backinfo.setdefault(guildid, []).append(playurl)
        a = len(backinfo[guildid])
        if a >= 3:
            backinfo.setdefault(guildid, []).pop(0)
    hadplay.setdefault(guildid, []).pop(0)
    # print(voice.is_playing())
    print("taskdone")
    time.sleep(1)
    if voice == None:
        print('disconnected')
        return
    elif not voice.is_playing():
        if isloop.get(guildid) == True:
            play_que.setdefault(guildid, []).insert(1,backinfo[guildid][-1])
            startplay(ctx)
        else:
            startplay(ctx)
         
    else:
        print('seek function in use ')


# get the song that just play before link   
@client.command(aliases=['before'])
###ANTI#SPAM##
async def beforeinfo(ctx):
    guildid = ctx.message.guild.id
    print(playurl)
    videoinfo = Video.getInfo(backinfo[guildid][-1], mode= ResultMode.json)
    
           
    await ctx.send(videoinfo['title'])
    await ctx.send("has been viewed")
    await ctx.send(videoinfo['viewCount']['text'] + " time")    
    # play_que.setdefault(guildid, []).insert(0,hadplay[guildid][0])
    # voice = get(client.voice_clients, guild=ctx.guild)
    # voice.stop()
    print('ok')

# play the prevoius song again
@client.command(aliases=['again'])
###ANTI#SPAM##
async def playthatagain(ctx):
    guildid = ctx.message.guild.id
    play_que.setdefault(guildid, []).insert(1,backinfo[guildid][-1])
              
    await ctx.send('ok that song will be play again')

# add the prevoius song to queue
@client.command()
###ANTI#SPAM##
async def addbefore(ctx):
    guildid = ctx.message.guild.id
    play_que.setdefault(guildid, []).append(backinfo[guildid][-1])
    
          
    await ctx.send("the previous song has now added to the queue!")

# loop the entire playlist
@client.command(aliases=['looplist'])
###ANTI#SPAM##
async def loopplaylist(ctx, logica=None):
    
        if logica is None:
            await ctx.send("loop? loop what? give me a number!\no(≧口≦)o")
        elif int(logica) <= 1000:
            guildid = ctx.message.guild.id
            for n in range(int(logica)):
                play_que.setdefault(guildid, []).extend(play_que[guildid])
                print(f"added {n}")
            await ctx.send(f"Alright, the entire playlist will be looped {logica} times!")
        else:
            await ctx.send("fuck off Girix L. Whitescale#3843")

# loop just the video 
@client.command()
###ANTI#SPAM##
async def loop(ctx, logica=None):
        if logica is None:
            guildid = ctx.message.guild.id
            if isloop.get(guildid) == True:
                isloop[guildid] = False
                await ctx.send('ok I had stopped the loop')
            if isloop.get(guildid) == False:
                isloop[guildid] = True
                await ctx.send('ok looping this song infinitely')
        elif int(logica) <= 1000:
            guildid = ctx.message.guild.id
            for n in range(int(logica)):
                play_que.setdefault(guildid, []).append(playurl)
                print(f"added {n}")
            await ctx.send(f"Alright, this song will be looped {logica} times!")
        else:
            await ctx.send("fuck off Girix L. Whitescale#3843")


@client.command(aliases=['isloop'])
###ANTI#SPAM##
async def isitloop(ctx):
    guildid = ctx.message.guild.id
    if isloop.get(guildid) == True:
        await ctx.send('I am in an loop')
    if isloop.get(guildid) == False:
        await ctx.send('I am not in a loop')

# my friend personal playlist
@client.command()
###ANTI#SPAM##
async def playitchy2020 (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
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
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s act 2!", "Ooo, my favorite!", "itchy's playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in url:
        a = b.replace('https://www.youtube.com/playlist?list=','')
        videos = scrapetube.get_playlist(a)
        for video in videos:
            # print("test")
            newstring = "https://www.youtube.com/watch?v=" + video['videoId']
            play_que.setdefault(guildid, []).append(newstring)
    # for item in url:
    #     video = Playlist(item)
    #     play_que.setdefault(guildid, []).append(video.videos)
    #     while video.hasMoreVideos:
    #         video.getNextVideos()
    #         play_que.setdefault(guildid, []).append(video.videos)
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)

###############custom playlist############################
# my friend personal playlist
@client.command()
###ANTI#SPAM##
async def playitchy2019 (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
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
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s act 1!", "wow, a classic!", "itchy's first playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in url:
        a = b.replace('https://www.youtube.com/playlist?list=','')
        videos = scrapetube.get_playlist(a)
        for video in videos:
            print("test")
            newstring = "https://www.youtube.com/watch?v=" + video['videoId']
            play_que.setdefault(guildid, []).append(newstring)
        print('ok')
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)

# my friend personal playlist
@client.command()
###ANTI#SPAM##
async def playitchys(ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()
    url = ['https://youtube.com/playlist?list=PLSJh9S2IPebGSSqkXACtbCJJcYc26Iy3i']
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s!", "nice pick!", "itchy's entire playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in url:
        a = b.replace('https://www.youtube.com/playlist?list=','')
        videos = scrapetube.get_playlist(a)
        for video in videos:
            print("test")
            newstring = "https://www.youtube.com/watch?v=" + video['videoId']
            play_que.setdefault(guildid, []).append(newstring)
        print('ok')
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)

# my personal playlist
@client.command()
###ANTI#SPAM##
async def playpooh (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()
    url = 'PLKu0PlxNFnZUjUzSxccTzHOgEYYGlSJk5'
    del play_que.setdefault(guildid, [])[:]
    pooh = ["Playing father playlist",'daddy favorite music']
    await ctx.send(random.choice(pooh)) 
    videos = scrapetube.get_playlist(url)
    for video in videos:
        print("test")
        newstring = "https://www.youtube.com/watch?v=" + video['videoId']
        play_que.setdefault(guildid, []).append(newstring)
        # while playlist:
        #     print('Getting more videos...')
        #     play_que.get(playlist.getVideos())
    print('ok')
    random.shuffle(play_que[guildid])
    random.shuffle(play_que[guildid])
    startplay(ctx)

###############custom playlist end ############################

@client.command()
async def testsend(ctx):
    async with ctx.typing():
        await asyncio.sleep(random.randint(int(0.1),int(0.9)))
    await ctx.send('testttt')

####setting command###
@client.command()
async def changeprofile(ctx):
    userid = ctx.message.author.id
    if int(admin_account) == userid:
        # print('sample string')
        initial_count = 0
        for path in pathlib.Path(imagedirpath).iterdir():
            if path.is_file():
                initial_count += 1
        n = random.randint(1,initial_count)
        pfp_path = imagedirpath + 'profile' + str(n) + '.jpg'
        print(pfp_path)
        fp = open(pfp_path, 'rb')
        pfp = fp.read()
        await client.user.edit(avatar=pfp)
        await ctx.send('user profile had been change')
    else:
        await ctx.send('you aint my master not following the order')

@client.command()
async def setstatus(ctx, *, status):
    userid = ctx.message.author.id
    if int(admin_account) == userid:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        await ctx.send(f'status changed to {status}')
    else:
        await ctx.send("you ait my dad don't tell me what to do lol")

@client.command()
async def update_song_embed(ctx):
    guildid = ctx.message.guild.id
    userid = int(ctx.message.author.id)
    print('ok bommer')
    if int(admin_account) == userid:
        if updatecurrentsong.get(guildid) == True:
            updatecurrentsong[guildid] = False
            await ctx.send('Ok stop sending update evertime newsong is playing')
        if updatecurrentsong.get(guildid) == False:
            update_song_embed[guildid] = True
            await ctx.send('Ok sending an update everytime new song is playing')
    else:
        pass



############ai stuff ############

@client.event
async def on_message(message):
    global ctx_react
    ctx_react = await client.get_context(message)
    await client.process_commands(message)

##### event stuff
@client.event
async def on_reaction_add(reaction, user):
    messageid = str(reaction.message.id)
    numbercounted = int(reaction.count)
    emoji = str(reaction.emoji)
    content = reaction.message.content
    # print(emoji)
    # print(messageid)
    # print(numbercounted)
    # print(content)
    if user != client.user:
        if messageid == reactid and emoji == "⏸️":
            await reaction.remove(user)
            await pause(ctx=ctx_react)
        if messageid == reactid and emoji == "▶️":
            await reaction.remove(user)
            await resume(ctx=ctx_react)
        if messageid == reactid and emoji == "⏭️":
            await reaction.remove(user)
            await skip(ctx=ctx_react)
        if messageid == reactid and emoji == "⏪":
            await reaction.remove(user)
            await playthatagain(ctx=ctx_react)
        if messageid == reactid and emoji == "🔁":
            await reaction.remove(user)
            await loop(ctx=ctx_react)

########error handling####
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('chill bro')
    else:
        pass
    
            
# @client.event
# async def on_reaction_remove(reaction, user):
#     pass
###########slash command begin#########


client.run(config['botsetting']['bot_token'])