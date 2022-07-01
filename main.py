# setup
import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import random
import operator
from titlecard import titlecard
from apikeys import *
import logging
import os
import json
import asyncio
import youtube_dl
import time
# logging and Operators
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.xor,
}
intents = discord.Intents.default()
intents.members = True
client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


"""This is a Section that is laggy for autoplaying music"""
# Dictionary for queueing songs
queues = {}

# works but is laggy
def check_queue(ctx, id):
    # if the server ID in the Dict has SONGS
    voice = ctx.guild.voice_client
    while queues[id] != []:
        # some reason this redundant check makes audio run with less stops
        if queues[id] != []:
            if not voice.is_playing():
                source = queues[id].pop(0)
                voice.play(source)

# code that i was experimenting with to autoplay and skip songs
def skip_song(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        voice.stop()
        source = queues[id].pop(0)
        voice.play(source)



# terminal message and title card when conencted
# sets the bot's activity to disply common command
@bot.event
async def on_ready():
    await bot.change_presence(
        status = discord.Status.idle, 
        activity = discord.Activity(
            type = discord.ActivityType.listening, 
            name = "!roll, !play"))
    titlecard(bot)  

# greets the user
@bot.listen('on_message')
async def greet(message):
    greetings = [
        'hey',
        'hello',
        'wassup',
        'hi',
        'bonjour',
        'hello there']
    if message.author == bot.user:
        return
    first_word = str(message.content).split(" ")[0]
    if any(greetings in str.lower(first_word) for greetings in greetings):
        await message.channel.send(f"{str.capitalize(random.choice(greetings))} {str(message.author).split('#')[0]}")
        print("Greeting Replied")       
# greets new memebers
@bot.event
async def on_member_join(member):
    channel = client.get_channel(986834387968598049)
    await channel.send(f"Hi {str(member.name).split('#')[0]}, welcome to the server")
# says Goodbye to leaving memebers
@bot.event
async def on_member_remove(member):
    channel = client.get_channel(986834387968598049)
    await channel.send(f"Goodbye {str(member.name).split('#')[0]}")

# user can roll dice with/without modifiers
"""
    Add a boolean variable that saves True or false to a global variable of TTS
    This allows for users to toggle TTS On/Off for the bot
"""
@bot.command()
async def roll(ctx, *args):
    print("Dice Being Rolled")
    # takes !roll argument, case insensitive
    # Examples: "!roll 1d20", "!roll 1d20 + 5"
    dice = str.lower(args[0])
    name = str(ctx.author).split("#")[0]
    num_of_dice = int(dice.split('d')[0])
    num_of_sides = int(dice.split('d')[1])
    result = []
    total = 0

    # rolls each dice and stores each random int in a list "result"
    for roll in range(num_of_dice):
        roll = random.randint(1, num_of_sides)
        result.append(roll)
        total += roll   
     
    # sort the result list from low to high
    result.sort()

    # string of the die rolls
    display_raw_roll = ["{}".format(result)]
    
    # if there is a modifier, apply after rolling
    if len(args) == 3:
        modifier = args[2]
        total = ops[args[1]](total, int(modifier))
        str_modifier = "{} {}".format(args[1], args[2])
        display_raw_roll = ["{} {}".format(result, str_modifier)]
    
    # checks if result is longer than 2000char message & prints the final total
    x = len(str(result))
    if x > 2000:
        await ctx.channel.send("Too many dice to handle!")
        return
    else:
        # shows user all dice rolls and modifier at end
        await ctx.channel.send(name + " Rolled: " + " {}".join(display_raw_roll))
        await ctx.channel.send(name + " Rolled a Total of **{}**".format(total), tts=True)
    
    # if user rolls a d20, records how many natural 20's were rolled
    if num_of_sides == 20:
        natty_count = 0
        for number in result:
            if number == 20:
                natty_count +=1
        if natty_count >= 2:
            await ctx.channel.send(f"**🎉 " + name + " Got {natty_count} Natural 20's!**", tts=True)
        elif natty_count == 1:
            await ctx.channel.send("**🎉 " + name + " Got a Natural 20!**", tts=True)

# bot joins user's channel && Plays notification audio
@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Audio\Bot_joined.wav')
        player = voice.play(source)
    else:
        await ctx.send('You are not connected to a voice channel for me to join!')
# bot leaves user's voice channel
@bot.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I left the voice channel')
    else:
        await ctx.send("I am not in a voice channel")

"""Music Bot Commands"""
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing in the voice channel")
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No audio is paused in the voice channel")
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()
@bot.command()
async def chill(ctx):
    # will join user channel and play chill.mp3
    # will play chill.mp3 if already in channel
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if (voice == None and ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Audio\chill.mp3')
    elif (voice != None and ctx.author.voice):
        source = FFmpegPCMAudio('Audio\chill.mp3')
    else:
        await ctx.send('You are not connected to a voice channel for me to join!')
    player = voice.play(source)

"""
    # !play "Arg" will play a file in Audio folder using filename as arg
    # added fucntionality to pass filename, no extension neeeded
    # function loops through audio folder and plays relevant audio
    # discord.utils.get returns None if it doesn't find anything. 
    # In this case, if voice is None, the bot isn't connected to any channel.
    # However, if your bot is connected, voice will be a discord
    # VoiceClient object, and the if statement will be executed.
"""
@bot.command()
async def play(ctx, arg):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
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
     
    voice.play(source, after = lambda x = None: check_queue(ctx, guild_id))

"""
    Queue Related Commands
"""
@bot.command()
async def queue(ctx, arg):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
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
@bot.command()
async def skip(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        skip_song(ctx, guild_id)
    else:
        ctx.send("There are no Songs left in the Queue")
@bot.command()
async def list(ctx):
    await ctx.send(queues)

"""
    Embed layout
    Concept = could use a JSON API of mosnter manual to take a command and provide an embed of a monster card
"""
@bot.command()
async def embed(ctx):
    embed = discord.Embed(
        title = "Title that has URL", 
        url = "https://www.dndbeyond.com/monsters/16988-quasit",
        description = "Description",
        color = 0x00FFFF
        )
    embed.set_author(
        name = ctx.author.display_name,
        url = "https://github.com/Devcon324",
        icon_url = ctx.author.avatar_url
        )
    embed.set_thumbnail(
        url = "https://www.dndbeyond.com/avatars/thumbnails/0/271/1000/1000/636252769318699115.jpeg"
        )
    embed.add_field(
        name = "AC",
        value = "13",
        inline = True
        )
    embed.add_field(
        name = "HP",
        value = "7",
        inline = True
        )
    embed.add_field(
        name = "Claws",
        value = "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d4 + 3) piercing damage, and the target must succeed on a DC 10 Constitution saving throw or take 5 (2d4) poison damage and become poisoned for 1 minute. The target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.",
        inline = False
        )
    embed.set_footer(
        text = "This is a Footer"
        )
    
    await ctx.send(embed=embed)

"""
    Error Catching
"""
@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed()
    # author not necessary, takes up too much space
    """embed.set_author(
        name = str(bot.user).split('#')[0],
        url = "https://github.com/Devcon324",
        icon_url = bot.user.avatar_url
        )"""
    embed.color = 0x00FFFF
    if isinstance(error, commands.MissingPermissions):
        embed.description = "You do not have permission to run this command"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandError):
        embed.description = "Something went wrong with this command"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed.description = "I am unsure what that command is. Try !help"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed.description = "Something went horribly wrong. Notify the Bot's Developer (https://github.com/Devcon324)"
        await ctx.send(embed=embed)

 
  



bot.run(BOTTOKEN)