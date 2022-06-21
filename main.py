import discord
from discord.ext import commands
from dice_roll import dice_roll
from music_cog import music_cog

Bot = commands.Bot(command_prefix='!')
Bot.add_cog(dice_roll(Bot))
Bot.add_cog(music_cog(Bot))


async def on_ready():
    print('We have logged in as {0.user}'.format(Bot))


with open("TOKEN.txt") as file:
    TOKEN = file.read()
Bot.run(TOKEN)