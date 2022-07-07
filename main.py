# setup
import discord
from discord.ext import commands
import os
from tools import TerminalCard, ActionLogger
from dotenv import load_dotenv
 
load_dotenv()

ActionLogger.log()

intents = discord.Intents.default()
intents.members = True
client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    # assigns a status to the bot's profile
    # shows commands it listens for
    await bot.change_presence(
        status = discord.Status.idle, 
        activity = discord.Activity(
            type = discord.ActivityType.listening, 
            name = "!roll, !play"))
    TerminalCard.title(bot)  

    # a list of cogs (.py file componenets of a bot)
    initial_extensions = []

    # loops through cog folder and loads cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            initial_extensions.append("cogs." + filename[:-3])
    print("Loading each COG into the bot")
    if __name__ == '__main__':
        for extension in initial_extensions:
            bot.load_extension(extension)
            print(extension)

bot.run(os.getenv("BOT_TOKEN"))
