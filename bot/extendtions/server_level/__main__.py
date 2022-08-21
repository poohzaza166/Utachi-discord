
from asyncio import tasks
import os
import discord
import yaml
from discord.ext import commands, tasks ,bridge
from discord.utils import get

from ...fileio import botconfig
from ...fileio import databasessavefile
from .lib.main import manager
from ...log import logs

# coding:utf-8
hexcolour = int(botconfig['bot_setting']['colour'],16)


enableid = botconfig['bot_setting']['levelguildid']

lv = manager(initxp=botconfig['bot_setting']['initxp'],charmuti=botconfig['bot_setting']['charmuti'])

adminacc = list(botconfig['bot_setting']['botadminacc'])


class level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        if os.path.exists(databasessavefile):
            lv.getaload()
            logs.info('loaded config file successfully')
        else:
            logs.info('no existing database were found')
        for guild in self.client.guilds:
            lv.registerguild(guild.id)
            # logs.info('ok')
        self.autobackup.start()
        logs.info('database self backup task successfully started')

    @commands.Cog.listener()
    async def on_message(self, message):
        guildid = message.guild.id
        author = message.author.id
        nameup = message.author.name
        mention = message.author.mention
        content = str(message.content)
        if message.author.bot:
            return
        else:
            if guildid in enableid:
                # logs.info(content)
                # blv = lv.checklevel(user=str(author))
                # logs.info(blv)
                lv.xpcal(guildid=guildid,user=str(author),message=content)
                q = lv.levelcal(guildid=guildid,user=str(author))
                if q == True:
                    a = lv.checklevel(guildid=guildid,user=str(author))
                    channel = self.client.get_channel(int(enableid.get(guildid)))
                    if lv.hadping(guildid=guildid,user=author) == False:
                        await channel.send(f'{nameup} you have reached level {a}')
                    if lv.hadping(guildid=guildid,user=author) == True:
                        await channel.send(f'{mention} {nameup} you have reached level {a}')

    @bridge.bridge_command(aliases=['top10','leaderboard'])
    async def leadboard(self, ctx):
        lead = lv.leaderboard(int(ctx.guild.id))
        board = {}
        j = 0
        output = []
        for key, val in lead.items():
            # logs.info(a)
            b = int(key)
            user = await self.client.fetch_user(b)
            logs.debug(user.name)
            board[user.name] = val
        for b, (n, i) in enumerate(board.items()):
            logs.debug(n)
            logs.debug(i)
            logs.debug(b)
            j =+ 1
            # if b == 0:
            #     p = 'Top Rank ' + n + ' Their level is ' + str(i)
            #     output.append(p)
            # if b >= 1:
            #     p = str(j) +') ' + n + ' Their level is ' + str(i)
            #     j =+ 1
            #     output.append(p)
            p = str(j) +') ' + n + ' Their level is ' + str(i)
            j =+ 1
            output.append(p)
        logs.debug(output)
        convertstr = str(output)[1:-1]
        outa = convertstr.replace(',', '\n')
        embeds = discord.Embed(title='Leader Board', description=outa, color=hexcolour)
        await ctx.send(embed=embeds)

    @bridge.bridge_command()
    async def annoying(self, ctx):
        await ctx.send(lv.toggleping(guildid=ctx.author.id,user=ctx.author.id))

    @bridge.bridge_command()
    async def isanoying(self, ctx):
        if lv.hadping(user=str(ctx.author.id),guildid=ctx.guild.id) == True:
            await ctx.send('pinging you when level up')
        if lv.hadping(user=str(ctx.author.id),guildid=ctx.guild.id) == False:
            await ctx.send('not pinging you when level up')

    @bridge.bridge_command(aliases=['lv','level'])
    async def checklevel(self, ctx):
        await ctx.send(f"your level is {str(lv.checklevel(guildid=ctx.guild.id,user=str(ctx.author.id)))}")

    @bridge.bridge_command(aliases=['xp'])
    async def checkxp(self, ctx):
        await ctx.send(f'your xp is {str(lv.checkxp(guildid=ctx.guild.id,user=str(ctx.author.id)))}')

    @bridge.bridge_command()
    async def setlevel(self, ctx, userid=None, number=None):
        if ctx.author.id in adminacc:
            if userid == None:
                await ctx.send('say who are you setting the level for')
            elif number == None:
                await ctx.send('give me a number for level lol')
            else:
                a = int(number)
                lv.setlevel(guildid=ctx.guild.id,user=str(userid),level=a)
        else:
            await ctx.send('No lol \n only bot owner can use this command')

    @bridge.bridge_command()
    async def setxp(self, ctx, userid, number=None):
        if ctx.author.id in adminacc:
            if number == None:
                await ctx.send('give me a number for xp lol')
            else:
                a = int(number)
                lv.setxp(guildid=ctx.guild.id,user=str(userid),level=a)
        else:
            await ctx.send('No lol \n only bot owner can use this command')

    @bridge.bridge_command()
    async def nextlv(self, ctx):
        a = lv.xpneedlv(guildid=ctx.guild.id,user=str(ctx.author.id))
        l = lv.checkxp(guildid=ctx.guild.id,user=str(ctx.author.id))
        c = a - l
        await ctx.send(f'xp require to reach next level is {a}')
        await ctx.send(f'your xp is {l}')
        await ctx.send(f'you currently need {c} more xp to level up!')

    @bridge.bridge_command()
    async def savestate(self, ctx):
        if ctx.author.id in adminacc:
            lv.savestate()
            await ctx.send('saved state successfully')
        else:
            await ctx.send('No lol \n only bot owner can use this command')

    @bridge.bridge_command()
    async def getaload(self, ctx):
        if ctx.author.id in adminacc:
            lv.getaload()
            await ctx.send('load save success')
        else:
            await ctx.send('No lol \n only bot owner can use this command')

    @tasks.loop(seconds=int(botconfig['bot_setting']['autobackup']))
    async def autobackup(a=None):
        logs.info('ok')
        lv.savestate
        logs.info('autobackup had been perform')

def setup(client):
    client.add_cog(level(client))
