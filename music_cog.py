import discord
from discord import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        #2D arreay containing [song, channel]
        self.music_queue = []
        self.YDL_OPTRIONS = {
            'format': 'bestaudio', 
            'noplaylist': 'True'
            }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnected_streamed 1 - reconnect_delay_max 5', 
            'options': '-vn'}
        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch: %s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {
            'source': info['formats'[0]['url']], 
            'title': info['title']
            }
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #gets the first URL for a video
            m_url = self.music_queue[0][0]['source']

            #remove the 0'th element in queue since you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), 
                after=lambda e: self.play_next()
                )
        else:
            self.is_playing = False
     
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #gets the first URL for a video
            m_url = self.music_queue[0][0]['source']

            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_comnnected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                self.vc = await self.bot.move_bot(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the 0'th element in queue since you are currently playing it

            self.music_queue.pop(0)
            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), 
                after=lambda e: self.play_next()
                )
        else:
            self.is_playing = False

    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        #if the user who authored the command is not in a channel
        if voice_channel is None:
            #you need ot be connected so that the bot knows where to go
            await ctx.send("You Must Connect to a Voice Channel First!")
        #if the user who authored the command is in a channel
        else:
            # search youtube with the query (can be a URL or keywords)
            # uses previous defined function to search
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect Format. Try Another Keyword. This Could be due to Playlist or a Livestram")
            else:
                await ctx.send("Song Added to the Queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def queue(self, ctx):
        #decalre a string
        retval = ""
        #iterate over every song in music_queue
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

            #print queue to consol
            print(retval)
            if retval != "":
                #print queue to Discord
                await ctx.send(retval)
            else:
                await ctx.send("No music in queue")
    
    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            #try to play next song in queue
            await self.play_music()