import pathlib
import random

import discord
from discord.ext import bridge
from discord.ext import commands

from ...fileio import botconfig
from ...log import logs
# coding:utf-8

adminacc = list(botconfig['bot_setting']['botadminacc'])

imager = 'config/profilepicture/'

class usermanager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logs.info('profile manager loaded')

    @bridge.bridge_command()
    async def amiadmin(self, ctx):
        userid = ctx.author.id
        if userid in adminacc:
            await ctx.send('yes you are an admin')
        else:
            await ctx.send('no you are not an admin')


    @bridge.bridge_command()
    async def change_profile(self, ctx):
        userid = ctx.author.id
        if userid in adminacc:
            a = 0
            for path in pathlib.Path(imager).iterdir():
                if path.is_file():
                    a += 1
            n = random.randint(1, a)
            pfp_path = imager + 'profile' + str(n) + '.jpg'
            fp = open(pfp_path, 'rb')
            pfp = fp.read()
            await self.client.user.edit(avatar=pfp)
            await ctx.send('user profile had been change')
        else:
            await ctx.send('you aint my master not following the order')

    @bridge.bridge_command()
    async def change_music_status(self, ctx, *,status):
        userid = ctx.author.id
        if userid in adminacc:
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
            await ctx.send(f'status changed to {status}')
        else:
            await ctx.send("you ait my dad don't tell me what to do lol")

    @bridge.bridge_command()
    async def change_game_status(self, ctx, *,status):
        userid = ctx.author.id
        if userid in adminacc:
            await self.client.change_presence(activity=discord.Game(status))
            await ctx.send(f'status changed to {status}')
        else:
            await ctx.send("you ait my dad don't tell me what to do lol")

    @bridge.bridge_command()
    async def ping(self, ctx):
        await ctx.send(f'here! {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(usermanager(client))
