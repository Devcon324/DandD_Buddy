import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os

""" This is a Section that is laggy for autoplaying music"""
# Dictionary for queueing songs"""
queues = {}
def check_queue(ctx, id):
    """This works perfectly, autoplays the queue until queue is empty"""
    if len(queues[id]) > 0:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        voice.play(source, after=lambda e: check_queue(ctx, id))

# code that i was experimenting with to autoplay and skip songs
def skip_song(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        voice.stop()
        source = queues[id].pop(0)
        voice.play(source)



class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    """
        # !play "Arg" will play a file in Audio folder using filename as arg
        # added fucntionality to pass filename, no extension neeeded
        # function loops through audio folder and plays relevant audio
        # discord.utils.get returns None if it doesn't find anything. 
        # In this case, if voice is None, the bot isn't connected to any channel.
        # However, if your bot is connected, voice will be a discord
        # VoiceClient object, and the if statement will be executed.
    """
    @commands.command()
    async def play(self, ctx, arg):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        guild_id = ctx.message.guild.id
        # join the voice channel if no already connected & play song
        if (voice == None and ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            for file in os.listdir('Audio'):
                if str.lower(arg) == str(file).split('.')[0]:
                    ext = str(file).split('.')[1]
                    source = FFmpegPCMAudio(f'Audio\{arg}.{ext}')
        # already in voice channel? then play the song
        elif (voice != None and ctx.author.voice):
            # declaring voice is not needed here
            # voice = ctx.guild.voice_client
            for file in os.listdir('Audio'):
                if str.lower(arg) == str(file).split('.')[0]:
                    ext = str(file).split('.')[1]
                    source = FFmpegPCMAudio(f'Audio\{arg}.{ext}')
        # user not in voice channel
        else:
            await ctx.send('You are not connected to a voice channel for me to join!')
        
        voice.play(source, after = lambda e: check_queue(ctx, guild_id))
    
    
    """
        Queue Related Commands
    """
    @commands.command()
    async def queue(self, ctx, arg):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        for file in os.listdir('Audio'):
                if str.lower(arg) == str(file).split('.')[0]:
                    ext = str(file).split('.')[1]
                    source = FFmpegPCMAudio(f'Audio\{arg}.{ext}')
        
        guild_id = ctx.message.guild.id
        
        # if the ID of our server is in the QUEUE Dict
        # then we want to add the song added to the Dict
        if guild_id in queues:
            # 'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]

        await ctx.send("Added to Queue")
    
    @commands.command()
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            skip_song(ctx, guild_id)
        else:
            ctx.send("There are no Songs left in the Queue")
    
    @commands.command()
    async def list(self, ctx):
        await ctx.send(queues)


    
    
    
    """Music Bot Commands"""
    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("No audio is playing in the voice channel")
    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("No audio is paused in the voice channel")
    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        voice.stop()
    @commands.command()
    async def chill(self, ctx):
        # will join user channel and play chill.mp3
        # will play chill.mp3 if already in channel
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if (voice == None and ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('Audio\chill.mp3')
        elif (voice != None and ctx.author.voice):
            source = FFmpegPCMAudio('Audio\chill.mp3')
        else:
            await ctx.send('You are not connected to a voice channel for me to join!')
        player = voice.play(source)

def setup(bot):
    bot.add_cog(MusicBot(bot))