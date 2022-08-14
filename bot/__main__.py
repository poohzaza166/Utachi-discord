from pprint import pprint
from sys import prefix

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import bridge

from .log import logs

from bot.fileio import botconfig

# coding:utf-8


client = commands.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())
# client = bridge.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())

client.remove_command("help")

@client.event
async def on_ready():
   logs.info('base class online')

@client.command()
async def help(ctx):
    await ctx.send('https://github.com/poohzaza166/Utachi-discord/wiki')

client.load_extension(name='bot.extendtions.music.__main__')
client.load_extension(name='bot.extendtions.profile.__main__')

if botconfig['bot_setting']['leveling'] == True:
    client.load_extension(name='bot.extendtions.server_level.__main__')
if botconfig['bot_setting']['luckgen'] == True:
    client.load_extension(name='bot.extendtions.misc.__main__')



client.run(botconfig['bot_setting']['bottoken'])

