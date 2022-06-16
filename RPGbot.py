import discord
import logging
from discord.ext import commands
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Since the on_message() event triggers for every message received, we have to make sure that we ignore messages from ourselves. 
# We do this by checking if the Message.author is the same as the Client.user.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)






bot.run('OTg2ODMzOTU1NTMxNjUzMTUw.Gma0XO.7cVBa6U6VhKMgwp-Zssm3EjYk9x96GSxZrMSNg')
client.run('OTg2ODMzOTU1NTMxNjUzMTUw.Gma0XO.7cVBa6U6VhKMgwp-Zssm3EjYk9x96GSxZrMSNg')