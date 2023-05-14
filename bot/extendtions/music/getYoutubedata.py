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