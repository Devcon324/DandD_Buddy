import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio
import youtube_dl

""" 
    Dictionary for queueing songs
    queues = {Guild_id: [song, song, song...]}
"""
queues = {}

def autoplay_queue(ctx, id):
    """This works, autoplays the queue until queue is empty"""
    if len(queues[id]) > 0:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        voice.play(source, after=lambda e: autoplay_queue(ctx, id))

"""code that i was experimenting with to autoplay and skip songs"""
def skip_song(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        voice.stop()
        source = queues[id].pop(0)
        voice.play(source)



class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YDL_OPTIONS = {
            'format': 'bestaudio', 
            'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'}
    

    """
        Queue Related Commands
    """
    """    @commands.command()
        async def queue(self, ctx, arg):
            voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
            guild_id = ctx.message.guild.id

            url = str(arg)

            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ytdl:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                song = data['url']

                source = discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS)
                    
            # if the ID of our server is in the QUEUE Dict
            # then we want to add the song added to the Dict
            if guild_id in queues:
                # 'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]

            await ctx.send("Added to Queue")"""


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

        url = str(arg)
        
        # join the voice channel if no already connected & play song
        if (voice == None and ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            
            if not guild_id in queues:
                queues[guild_id] = []

            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ytdl:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                song = data['url']
                source = discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS)
            
                if voice.is_playing():
                    # if the ID of our server is in the QUEUE Dict
                    # then we want to add the song added to the Dict
                    if guild_id in queues:
                        # 'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
                        queues[guild_id].append(source)
                    else:
                        queues[guild_id] = [source]

                    await ctx.send("Added to Queue")
                else:
                    voice.play(source, after = lambda e: autoplay_queue(ctx, guild_id))
        
        # already in voice channel? then get the source
        elif (voice != None and ctx.author.voice):
            # moves the bot to the client's voice channel
            channel = ctx.message.author.voice.channel
            await voice.move_to(channel)

            if not guild_id in queues:
                queues[guild_id] = []

            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ytdl:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                song = data['url']
                source = discord.FFmpegPCMAudio(song, **self.FFMPEG_OPTIONS)

                if voice.is_playing():
                    # if the ID of our server is in the QUEUE Dict
                    # then we want to add the song added to the Dict
                    if guild_id in queues:
                        # 'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
                        queues[guild_id].append(source)
                    else:
                        queues[guild_id] = [source]

                    await ctx.send("Added to Queue")
                else:
                    voice.play(source, after = lambda e: autoplay_queue(ctx, guild_id))
                
        # user not in voice channel
        else:
            await ctx.send('You are not connected to a voice channel for me to join!')
        
        
    
    
    
    @commands.command()
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        guild_id = ctx.message.guild.id

        if guild_id in queues:
            skip_song(ctx, guild_id)
            ctx.send("Audio Skipped")
        else:
            ctx.send("There are no Songs left in the Queue")
    
    @commands.command()
    async def list(self, ctx):
        await ctx.send(queues)


    
    
    
    """Music Bot Commands"""
    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        guild_id = ctx.message.guild.id

        if voice.is_playing() and guild_id in queues:
            voice.pause()
        else:
            await ctx.send("No audio is playing in the voice channel")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        guild_id = ctx.message.guild.id

        if voice.is_paused() and guild_id in queues:
            voice.resume()
        else:
            await ctx.send("No audio is paused in the voice channel")
            
    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        voice.stop()
        guild_id = ctx.message.guild.id

        if guild_id in queues:
            queues[guild_id] = []






    """Custom Bot Commands"""
    @commands.command()
    async def chill(self, ctx):
        # will join user channel and play chill.mp3
        # will play chill.mp3 if already in channel
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if (voice == None and ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('audio\chill.mp3')
        elif (voice != None and ctx.author.voice):
            source = FFmpegPCMAudio('audio\chill.mp3')
        else:
            await ctx.send('You are not connected to a voice channel for me to join!')
        player = voice.play(source)

def setup(bot):
    bot.add_cog(MusicBot(bot))




    """
    
    {
        'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
        'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
        'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
        'Guild_ID': ['Song_0', 'Song_1', 'Song_2'],
    }
    
    
    """