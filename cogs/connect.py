import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio


class Connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    # bot joins user's channel && Plays notification audio
    @commands.command()
    async def join(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('Audio\Bot_joined.wav')
            player = voice.play(source)
        else:
            await ctx.send('You are not connected to a voice channel for me to join!')
    
    # bot leaves user's voice channel
    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if (ctx.voice_client):
            channel = ctx.message.author.voice.channel
            source = FFmpegPCMAudio('Audio\Bot_leave.wav')
            player = voice.play(source)
            await asyncio.sleep(2.5)
            await ctx.guild.voice_client.disconnect()
            await ctx.send('I left the voice channel')
        else:
            await ctx.send("I am not in a voice channel")

def setup(bot):
    bot.add_cog(Connect(bot))