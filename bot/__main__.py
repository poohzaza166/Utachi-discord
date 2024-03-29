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

import asyncio
import random

import discord
from discord.ext import bridge, commands
from discord.utils import get
# from discord.ext.bridge import BridgeExtContext

from bot.fileio import botconfig

from bot.log import logs

# coding:utf-8



typani = []

# class Pcontext(bridge.BridgeExtContext):
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
                dtime = ((botconfig['bot_setting']['aniwpm']) / len(wd_ls)) + random.randint(int(botconfig['bot_setting']['animin']),int(botconfig['bot_setting']['animax']))
                logs.info(f'delaying animation for {dtime} second')
                await asyncio.sleep(dtime)
            if embed == None:
                await self.reply(msg)
            elif embed != None:
                await self.reply(embed=embed)
        else:
            if embed == None:
                await self.reply(msg)
            elif embed != None:
                await self.reply(embed=embed)

class APcontext(bridge.BridgeApplicationContext):
    def __init__(self, bot, interaction):
        super().__init__(bot, interaction)
        # self.message = discord.message()
        # self.message.guild = interaction.guild
        # self.message.author = interaction.authors
        # self.message.channel = interaction.channel
        # self.message = discord.message()
        # self.message.guild = self.guild
        # self.message.author = self.author

# class CUbot(discord.bot):
class CUbot(bridge.Bot):
    async def get_context(self, message: discord.Message, *, cls=Pcontext):
        return await super().get_context(message,cls=cls)

    async def get_application_context(self, interaction: discord.Interaction, cls=APcontext):
        # The same method for custom application context.
        return await super().get_application_context(interaction, cls=cls)

# class BOTBRIDGE(bridge.Bot):
#     async def get_context(self, message: discord.Message, cls=Pcontext) -> BridgeExtContext:
#         return await super().get_context(message, cls=cls)

def run():

    client = CUbot(command_prefix=commands.when_mentioned_or(botconfig['bot_setting']['botprefix']), intents=discord.Intents.all())
    # client = commands.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())
    # client = bridge.Bot(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())
    # client = BOTBRIDGE(command_prefix=botconfig['bot_setting']['botprefix'], intents=discord.Intents.all())


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
        guildid = ctx.guild.id
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
    if botconfig['bot_setting']['dislikelookup'] == True:
        client.load_extension(name="bot.extendtions.music.getYoutubedata")

    client.run(botconfig['bot_setting']['bottoken'])

if __name__ == '__main__':
    run()

