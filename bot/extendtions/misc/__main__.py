import random

from discord.ext import commands
from discord.ext import bridge
# coding:utf-8

class luckgen(commands.Cog):

    def __init__(self, client):
        self.client = client


    @bridge.bridge_command(aliases=['8ball'])
    async def magic8ball( self ,ctx, *, question):
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @bridge.bridge_command()
    async def dnd_dice( self ,ctx):
        responses = ["1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "6",
                     "7",
                     "8",
                     "9",
                     "10",
                     "11",
                     "12",
                     "13",
                     "14",
                     "15",
                     "16",
                     "17",
                     "18",
                     "19",
                     "20"]
        await ctx.send(f'{random.choice(responses)}/20')

    @bridge.bridge_command(aliases=['coin'])
    async def coin_flip( self ,ctx):
        responses = ["Heads",
                     "Tails"]
        await ctx.send(f'{random.choice(responses)}!')

def setup(client):
    client.add_cog(luckgen(client))
