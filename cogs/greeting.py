import discord
from discord.ext import commands
import random


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # greets the user
    """Bug - will greet even if soemone types abcHEYefg"""
    @commands.Cog.listener('on_message')
    async def greet(self, message):
        greetings = [
        'hey',
        'hello',
        'wassup',
        'hi',
        'bonjour',
        'hello there']
        if message.author == self.bot.user:
            return
        first_word = str(message.content).split(" ")[0]
        if any(greetings in str.lower(first_word) for greetings in greetings):
            await message.channel.send(f"{str.capitalize(random.choice(greetings))} {str(message.author).split('#')[0]}")
            print("Greeting Replied") 

    # greets new memebers
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(986834387968598049)
        await channel.send(f"Hi {str(member.name).split('#')[0]}, welcome to the server")
    
    # says Goodbye to leaving memebers
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(986834387968598049)
        await channel.send(f"Goodbye {str(member.name).split('#')[0]}")

def setup(bot):
    bot.add_cog(Greetings(bot))