from os import sync
from pprint import pprint
import random

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import bridge
import asyncio
from .log import logs

from bot.fileio import botconfig

# coding:utf-8

typani = []


class Pcontext(commands.Context):
    async def send(self, msg=None, embed=None):
        logs.debug(f'ok printing {msg}')
        if self.message.guild.id in typani:
            async with self.message.channel.typing():
                try:
                    wd_ls = msg.split()
                except AttributeError:
                    wd_ls = str(embed.description).split()
                    # wd_ls = ['1']
                dtime = ((botconfig['bot_setting']['aniwpm']/60) * len(wd_ls)) + random.randint(int(botconfig['bot_setting']['animin']),int(botconfig['bot_setting']['animax']))
                logs.info(f'delaying animation for {dtime} second')
                await asyncio.sleep(dtime)
            if embed == None:
                await self.message.channel.send(msg)
            elif embed != None:
                await self.message.channel.send(embed=embed)
        else:
            if embed == None:
                await self.message.channel.send(msg)
            elif embed != None:
                await self.message.channel.send(embed=embed)

# class APcontext(discord.ApplicationContext):

class CUbot(commands.Bot):
    async def get_context(self, message: discord.Message, *, cls=Pcontext):
        return await super().get_context(message,cls=cls)

def run():

    client = CUbot(command_prefix=commands.when_mentioned_or(botconfig['bot_setting']['botprefix']), intents=discord.Intents.all())
    # client = commands.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())
    # client = bridge.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())

    client.remove_command("help")

    @client.event
    async def on_ready():
        print('base class online')
        logs.info('base class online')

    @client.command()
    async def help(ctx):
        await ctx.send('https://github.com/poohzaza166/Utachi-discord/wiki')

    @client.command()
    async def animation(ctx):
        guildid = ctx.message.guild.id
        if guildid in typani:
            await ctx.send('disabling typing animation')
            typani.remove(guildid)
        else:
            await ctx.send('enabling typing animation')
            typani.append(guildid)

    client.load_extension(name='bot.extendtions.music.__main__')
    client.load_extension(name='bot.extendtions.profile.__main__')

    if botconfig['bot_setting']['leveling'] == True:
        client.load_extension(name='bot.extendtions.server_level.__main__')
    if botconfig['bot_setting']['luckgen'] == True:
        client.load_extension(name='bot.extendtions.misc.__main__')


    client.run(botconfig['bot_setting']['bottoken'])

if __name__ == '__main__':
    run()

