from ...fileio import botconfig
from ...log import logs
from .lib.yt_data import parse_data

from discord.ext import bridge
from discord.ext import commands


class getYoutubedata(commands.Cog):
    def __init__(self, client):
        logs.info("yt stats class online")

    @bridge.bridge_command(aliases=['dislike'])
    async def lookup(self, ctx, url=None):
        if "https://www.youtube.com" in url:
            song = parse_data(url)
            await ctx.send(f'''
the video is {song['videoname']}
...and it has been viewed {song['view']} times!
also here's the link! --> {url}
which have {song["like"]} like
... and a {song["dislike"]}''')
        elif "https://youtu.be/":
            newurl = "https://www.youtube.com/watch?v="
            newurl.join(url.replace("https://youtu.be",""))
            song = parse_data(newurl)
            await ctx.send(f'''
the video is {song['videoname']}
...and it has been viewed {song['view']} times!
also here's the link! --> {url}
which have {song["like"]} like
... and a {song["dislike"]}''')
        else:
            await ctx.send("please send a youtube link please")

def setup(client):
    client.add_cog(getYoutubedata(client))