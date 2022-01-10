from __future__ import unicode_literals
from asyncio.tasks import create_task
import logging
import os
from discord.ext.commands.errors import CommandError
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
config_string =  'config.ini'
abspath = os.path.abspath(config_string)
config =  configparser.ConfigParser()
# print(abspath)
config.read(abspath)
config.sections()

client = discord.Client()
# print(config['botsetting']['bot_token'])
client = commands.Bot(command_prefix=config['botsetting']['bot_prefix'])  # prefix our commands with '.'
client.remove_command("help")

play_que = {}
hadplay = {}
backinfo = {}

# timestamp = '1:20'
   
#respond list for itchy 
reply = ['alright, see you soon!',"oh no, it's time to go?","utachi...\nout!"]
replybfr = ['owh please let me play a few hundred songs before i go—', "what why— that song was great!","what why— things were getting good!","hey! i am not finished yet!"]
replyf = ["meanie beanie!\n.·´¯`(>▂<)´¯`·. ","imma go cry in my digital corner (┬┬﹏┬┬)","GRrrrrr, that's it!\n💨","i have robotic feelings you know!","``` css red Fine!```","what an angry baby you are!"]
shuffleres = ['Okay, shuffling the queue...','shaking it up!','order is now nonexistent.','RNG time baby~']
replyskip = ["yup let's!",'finally!','Hey, we were at the good part!','b-but that song was nice…','song skipped!','sure can do!','```css \n red KING CRIMSON!```']
replypause = ['``` css yellow ZA WARUDO!```','Okay!','am i too loud for you?','music break?','stopped.']
manunal = ""

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
# global channels
# global voice
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, CommandError):
#         await ctx.reply("command not found or invalid syntax \n use -man for info")

# check if bot is ready
@client.event  
async def on_ready():
    print('Bot online')


# command for bot to join the channels of the user, if the bot has already joined and is in a different channels, it will move to the channels the user is in
@client.command(aliases=['come', 'cum'])
async def join(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

def random_time():
    return random.randint(1,2)

# leave command
@client.command()
async def leave(ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)    
    if voice.is_playing():
        await ctx.reply(random.choice(replybfr))
        await ctx.guild.voice_client.disconnect()
        async with ctx.typing():
            await asyncio.sleep(random_time())
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
    else:
        await ctx.reply(random.choice(reply))
        await ctx.guild.voice_client.disconnect()
        async with ctx.typing():
            await asyncio.sleep(random_time())
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]

# rude leave
@client.command()
async def fuckoff(ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)    
    if voice.is_connected():
        await ctx.reply(random.choice(replyf))
        await ctx.guild.voice_client.disconnect() # Leave the channels
        async with ctx.typing():
            await asyncio.sleep(random_time())
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]
    else:
        await ctx.reply(random.choice(replyf))
        await ctx.guild.voice_client.disconnect() # Leave the channels
        async with ctx.typing():
            await asyncio.sleep(random_time())
        await ctx.send('``>Bot left``')
        del play_que.setdefault(guildid, [])[:]

# manunal command
@client.command()
async def man(ctx):
    await ctx.send(manunal)

# abit of easter egg
@client.command()
async def groovy(ctx, *, a):
    async with ctx.typing():
        await asyncio.sleep(random_time())
    await ctx.send('wrong person he not here')

# shuffle command
@client.command(aliases=['clear'])
async def shuffle(ctx):
    guildid = ctx.message.guild.id
    random.shuffle(play_que.setdefault(guildid, []))
    async with ctx.typing():
        await asyncio.sleep(random_time())
    await ctx.send(random.choice(shuffleres))

# clear playlist command 
@client.command()
async def clearlist(ctx):
    clearlistres = ["gotchu, list cleared!"]# edit shit here
    guildid = ctx.message.guild.id
    del play_que.setdefault(guildid, [])[:]
    async with ctx.typing():
        await asyncio.sleep(random_time())
    await ctx.send(random.choice(clearlistres))

# remove the last song from playlist
@client.command()
async def bremove(ctx):
    bremoveres = ["gotchu, I have removed the last song!"]
    guildid = ctx.message.guild.id
    del play_que.setdefault(guildid, [])[-1]
    async with ctx.typing():
        await asyncio.sleep(random_time())
    await ctx.send(random.choice(bremoveres))

# check the song in queue
@client.command()
async def queue(ctx):
    async with ctx.typing():
        guildid = ctx.message.guild.id
        j = 0
        now_playing = play_que.get(guildid)
        listofplay = []
        actual2 = []
        if len(now_playing) == 0:
            await ctx.send("no song in queue")
        elif len(now_playing) < 6:
            ammountoftime = len(now_playing)
        else:
            ammountoftime = 6
        # await ctx.send(now_playing)
        print(ammountoftime)
        print(now_playing[0])
        for n in range(ammountoftime):
            if n == 0:
                pass
            else:
                print(n)
                print(now_playing[n])
                video = Video.get(now_playing[n])
                listofplay.append(video['title'])
        print(listofplay)
        for i in listofplay:
            j += 1
            test = str(j) + ') ' + i
            actual2.append(test)
        print("--------------------------------")
        print(actual2)
        print("--------------------------------")
        convertstring = str(actual2)[1:-1]
        print(convertstring)
        print("--------------------------------")
        actuallist = convertstring 
        print(actuallist.replace(',', "\n" ))
        list1 = actuallist.replace(',', '\n' )
        # for i in list1:
        #     j += 1
        #     finalque = str(j) + ')' + i  
        currnetsong =  Video.getInfo(playurl, mode= ResultMode.json)
        if len(now_playing) < 5:            
            await ctx.send(f"``` now playing {currnetsong['title']}\n{list1}```")  
        else:
            await ctx.send(f"``` now playing {currnetsong['title']}\n{list1} \n and more playing```") 
    # for n in now_playing:
    #     video = await Video.get(now_playing[n])
    #     print(video)
    #     listofplay.append


# command to play sound from a youtube URL
@client.command(pass_context=True,aliases=['p'])
async def play(ctx, *, url):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)    
    if "https://www.youtube.com/playlist?list=" in url:
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
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send("gotchu, playlist is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this playlist will be play next ')

    elif "https://" in url:
        print('it a url')
        play_que.setdefault(guildid, []).append(url)
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send ("alright this video will be play next")


    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).append(videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this video will be play next')

# command to play sound from a youtube URL next 
@client.command(pass_context=True,aliases=['pnext'])
async def playnext(ctx, *, url):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)    
    if "https://www.youtube.com/playlist?list=" in url:
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
            async with ctx.typing():
                await asyncio.sleep(random_time())      
            await ctx.send("gotchu, playlist is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this playlist will be play next ')

    elif "https://" in url:
        print('it a url')
        play_que.setdefault(guildid, []).insert(0,url)
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send ("alright this video will be play next")


    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).insert(0,videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this video will be play next')

# command to play sound from a youtube URL now
@client.command(pass_context=True,aliases=['pnow'])
async def playnow(ctx, *, url):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()

    print(url)    
    if "https://www.youtube.com/playlist?list=" in url:
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
            async with ctx.typing():
                await asyncio.sleep(random_time())      
            await ctx.send("gotchu, playlist is now playing!")
        else:
            voice.stop()
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this playlist will be play now ')

    elif "https://" in url:
        print('it a url')
        play_que.setdefault(guildid, []).insert(0,url)
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send(f"gotchu, {url} is now playing!")
        else:
            voice.stop()
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send ("alright this video will be play now")


    else: 
        print("normal video search")
        videosSearch = VideosSearch(url , limit = 1, language = 'en', region = 'UK')
        videosResult = await videosSearch.next()
        print(videosResult)
        print(videosResult['result'][0]['link'])
        play_que.setdefault(guildid, []).insert(0,videosResult['result'][0]['link'])
        if not voice.is_playing():
            startplay(ctx)
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send("gotchu, "+ videosResult['result'][0]['title']  + "is now playing!")
        else:
            voice.stop()
            async with ctx.typing():
                await asyncio.sleep(random_time())   
            await ctx.send('alright this video will be play now')


# get the song url 
@client.command(aliases=['sauce'])
async def warp(ctx):
    guildid = ctx.message.guild.id
    print(playurl)
    async with ctx.typing():
        await asyncio.sleep(random_time())   
    await ctx.send("the current song link playing is " + playurl)


# skip the song in playlist
@client.command(aliases=['next','kingcrimson!','foward'])
async def skip(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        async with ctx.typing():
            await asyncio.sleep(random_time())   
        await ctx.send(random.choice(replyskip))
        # play_next(ctx)


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
        async with ctx.typing():
            await asyncio.sleep(random_time())   
        await ctx.send('the music is resuming!')


# command to pause voice if it is playing
@client.command(aliases=['stop'])
async def pause(ctx):
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        async with ctx.typing():
            await asyncio.sleep(random_time())   
        await ctx.send(random.choice(replypause))

# give the current song info 
@client.command(aliases=['current','song','info'])
async def currentsonginfo(ctx, song=0):
    guildid = ctx.message.guild.id
    songq = play_que[guildid][song]
    print(songq)
    videoinfo = Video.getInfo(songq, mode= ResultMode.json)
    # print(videoinfo)
    async with ctx.typing():
        await asyncio.sleep(random_time())   
    await ctx.send(f'song in queue number {song}')
    await ctx.send("the current song playing is: " + videoinfo['title'])
    await ctx.send("...and it has been viewed " + videoinfo['viewCount']['text'] + " times!")
    await ctx.send ("also here's the link! --> " + songq)

# my friend personal playlist
@client.command()
async def playitchy2020 (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()
    url = ['https://www.youtube.com/playlist?list=PLQJHbSBLRWJSPZjTDPaIaLXpM7-JMI7RG', 'https://www.youtube.com/playlist?list=PLQJHbSBLRWJQuWq0QTB02dcemPwQlMUTJ','https://www.youtube.com/playlist?list=PLQJHbSBLRWJSV2Ocjftmp1ekoIXBFjXTs','https://www.youtube.com/playlist?list=PLQJHbSBLRWJT5mm_k0kfgzF0jEBaJOGAK','https://www.youtube.com/playlist?list=PLQJHbSBLRWJR75XSSvSSv7SlA6BY-ZZsd' ]
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s act 2!", "Ooo, my favorite!", "itchy's playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in range(5):
        print('playing itch')
        print(b)
        playlist = Playlist.getVideos(url[b])
        timesa = Playlist(url[b]) 
        times = len(timesa.videos)
        # play_que.get(await playlist.getVideos(url))
        print('command checkpoint')
        # print(playlist)
        # print(times)
        for n in range(times):
            print("command ")
            print(playlist['videos'][n]['link'])
            play_que.setdefault(guildid, []).append(playlist['videos'][n]['link'])
        # while playlist:
        #     print('Getting more videos...')
        #     play_que.get(playlist.getVideos())
        print('ok')
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)

# my friend personal playlist
@client.command()
async def playitchy2019 (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()
    url = ['https://www.youtube.com/playlist?list=PLQJHbSBLRWJQS-q5yFzhxo3ibjFYREuvI', 'https://www.youtube.com/playlist?list=PLQJHbSBLRWJTPyj6wUe72-UdJEBEcQW2_','https://www.youtube.com/playlist?list=PLQJHbSBLRWJQfxi0ry3VnnioDvOCfODgF','https://www.youtube.com/playlist?list=PLQJHbSBLRWJRpoPK3MMtNy2JkxhbjRAE3','https://www.youtube.com/playlist?list=PLQJHbSBLRWJQZo3ab7BEZW4gDWyaSKmWn','https://www.youtube.com/playlist?list=PLQJHbSBLRWJR4AHkFx4sK8QKU5lWBiioU','https://www.youtube.com/playlist?list=PLQJHbSBLRWJRX8mSWWwtLgSVy5sf_2GnH']
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s act 1!", "wow, a classic!", "itchy's first playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in range(len(url)):
        print('playing itch')
        print(b)
        playlist = Playlist.getVideos(url[b])
        timesa = Playlist(url[b]) 
        times = len(timesa.videos)
        # play_que.get(await playlist.getVideos(url))
        print('command checkpoint')
        # print(playlist)
        # print(times)
        for n in range(times):
            print("command ")
            print(playlist['videos'][n]['link'])
            play_que.setdefault(guildid, []).append(playlist['videos'][n]['link'])
        # while playlist:
        #     print('Getting more videos...')
        #     play_que.get(playlist.getVideos())
        print('ok')
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)

# my friend personal playlist
@client.command()
async def playitchys (ctx):
    guildid = ctx.message.guild.id
    channels = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channels)
    else:
        voice = await channels.connect()
    url = ['https://www.youtube.com/playlist?list=PLQJHbSBLRWJQS-q5yFzhxo3ibjFYREuvI', 'https://www.youtube.com/playlist?list=PLQJHbSBLRWJTPyj6wUe72-UdJEBEcQW2_','https://www.youtube.com/playlist?list=PLQJHbSBLRWJQfxi0ry3VnnioDvOCfODgF','https://www.youtube.com/playlist?list=PLQJHbSBLRWJRpoPK3MMtNy2JkxhbjRAE3','https://www.youtube.com/playlist?list=PLQJHbSBLRWJQZo3ab7BEZW4gDWyaSKmWn','https://www.youtube.com/playlist?list=PLQJHbSBLRWJR4AHkFx4sK8QKU5lWBiioU','https://www.youtube.com/playlist?list=PLQJHbSBLRWJRX8mSWWwtLgSVy5sf_2GnH','https://www.youtube.com/playlist?list=PLQJHbSBLRWJSPZjTDPaIaLXpM7-JMI7RG','https://www.youtube.com/playlist?list=PLQJHbSBLRWJQuWq0QTB02dcemPwQlMUTJ','https://www.youtube.com/playlist?list=PLQJHbSBLRWJSV2Ocjftmp1ekoIXBFjXTs','https://www.youtube.com/playlist?list=PLQJHbSBLRWJT5mm_k0kfgzF0jEBaJOGAK','https://www.youtube.com/playlist?list=PLQJHbSBLRWJR75XSSvSSv7SlA6BY-ZZsd']
    del play_que.setdefault(guildid, [])[:]
    itchrandom_respond = ["Playing itchy’s!", "nice pick!", "itchy's entire playlist huh?\ngotchu!"]
    await ctx.send(random.choice(itchrandom_respond)) 
    for b in range(12):
        print('playing itch')
        print(b)
        playlist = Playlist.getVideos(url[b])
        timesa = Playlist(url[b]) 
        times = len(timesa.videos)
        # play_que.get(await playlist.getVideos(url))
        print('command checkpoint')
        # print(playlist)
        # print(times)
        for n in range(times):
            print("command ")
            print(playlist['videos'][n]['link'])
            play_que.setdefault(guildid, []).append(playlist['videos'][n]['link'])
        # while playlist:
        #     print('Getting more videos...')
        #     play_que.get(playlist.getVideos())
        print('ok')
    random.shuffle(play_que[guildid])
    play_que.setdefault(guildid, []).pop(0)
    random.shuffle(play_que[guildid])
    startplay(ctx)


# my personal playlist
@client.command()
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

# debug command 
@client.command()
async def view(ctx):
    print(play_que)
    print("------------------------------------")
    print(hadplay)
    print("------------------------------------")
    print(backinfo)

# count the current song in playlist
@client.command(aliases=['songcount', 'total'])
async def count(ctx):
    guildid = ctx.message.guild.id
    await ctx.send("counting...")
    async with ctx.typing():
        await asyncio.sleep(random_time())   
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
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(playurl, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))   
            voice.is_playing()
            print('playing')
            # backinfo.setdefault(guildid, []).pop(0)
    else:
        asyncio.run_coroutine_threadsafe(suck(ctx), _loop)
#function       
async def suck(ctx):
    await ctx.send('no more music in playlist')

# debug command
# @client.command()
# async def printp(ctx):
#     print(playurl)

# skip to parts in song 
@client.command()
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
            async with ctx.typing():
                await asyncio.sleep(random_time())
            await ctx.send(f'skiped to {timestamp}')   
        else:
            pass
        
# function
def play_next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    guildid = ctx.message.guild.id
    # time.sleep(5)
    play_que.setdefault(guildid, []).pop(0)
    if not guildid in backinfo:
        backinfo.setdefault(guildid, []).append(playurl)
    elif playurl != backinfo[guildid][-1]:
        backinfo.setdefault(guildid, []).append(playurl)
        a = len(backinfo[guildid])
        if a >= 3:
            backinfo.setdefault(guildid, []).pop(0)
    hadplay.setdefault(guildid, []).pop(0)
    print(voice.is_playing())
    print("taskdone")
    time.sleep(1)
    if not voice.is_playing():
        startplay(ctx)
    else:
        print('seek function in use ')

# get the song that just play before link   
@client.command(aliases=['before'])
async def beforeinfo(ctx):
    guildid = ctx.message.guild.id
    print(playurl)
    videoinfo = Video.getInfo(backinfo[guildid][-1], mode= ResultMode.json)
    async with ctx.typing():
        await asyncio.sleep(random_time())   
    await ctx.send(videoinfo['title'])
    await ctx.send("has been viewed")
    await ctx.send(videoinfo['viewCount']['text'] + " time")    
    # play_que.setdefault(guildid, []).insert(0,hadplay[guildid][0])
    # voice = get(client.voice_clients, guild=ctx.guild)
    # voice.stop()
    print('ok')

# play the prevoius song again
@client.command(aliases=['again'])
async def playthatagain(ctx):
    guildid = ctx.message.guild.id
    play_que.setdefault(guildid, []).insert(1,backinfo[guildid][-1])
    async with ctx.typing():
        await asyncio.sleep(random_time())   
    await ctx.send('ok that song will be play again')

# add the prevoius song to queue
@client.command()
async def addbefore(ctx):
    guildid = ctx.message.guild.id
    play_que.setdefault(guildid, []).append(backinfo[guildid][-1])
    async with ctx.typing():
        await asyncio.sleep(random_time())   
    await ctx.send("the previous song has now added to the queue!")

# loop the entire playlist
@client.command(aliases=['looplist'])
async def loopplaylist(ctx, logica=None):
    async with ctx.typing():
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
async def loop(ctx, logica=None):
    async with ctx.typing():
        if logica is None:
            await ctx.send("loop? loop what? give me a number!\no(≧口≦)o")
        elif int(logica) <= 1000:
            guildid = ctx.message.guild.id
            for n in range(int(logica)):
                play_que.setdefault(guildid, []).append(playurl)
                print(f"added {n}")
            await ctx.send(f"Alright, this song will be looped {logica} times!")
        else:
            await ctx.send("fuck off Girix L. Whitescale#3843")



            
client.run(config['botsetting']['bot_token'])
