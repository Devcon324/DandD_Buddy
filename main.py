import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import random
import operator
from titlecard import titlecard
from apikeys import *
import requests
import json
import os
import asyncio
import youtube_dl
import time

#setup
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

@bot.event
async def on_ready():
    titlecard(bot)

# greets the user
@bot.command()
async def hello(ctx):
    greetings = [
        'Hey',
        'Hello',
        'Wassup',
        'Hi',
        'Bonjour',
        'Hello there, ']
    await ctx.channel.send(f"{random.choice(greetings)} {str(ctx.author).split('#')[0]}, I am {bot.user}")

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

# takes !roll argument, case insensitive
# Examples: "!roll 1d20", "!roll 1d20 + 5"
@bot.command(pass_context = True)
async def roll(ctx, *args):
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
            await ctx.channel.send("**🎉 " + name + " Got {} Natural 20's!**".format(natty_count), tts=True)
        elif natty_count == 1:
            await ctx.channel.send("**🎉 " + name + " Got a Natural 20!**", tts=True)

# bot joins user's channel && Plays an audio file
@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Audio\Bot_joined.wav')
        player = voice.play(source)
    else:
        await ctx.send('You are not connected to a voice channel for me to join!')
    
# bot leaves user's voice channel
@bot.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I left the voice channel')
    else:
        await ctx.send("I am not in a voice channel")







"""Music Bot Commands"""
@bot.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing in the voice channel")

@bot.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No audio is paused in the voice channel")

@bot.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    voice.stop()

# !play "Arg" will play a file in Audio folder using filename as arg
# added fucntionality to pass filename, no extension neeeded
# function loops through audio folder and plays relevant audio
@bot.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    for file in os.listdir('Audio'):
        if str.lower(arg) == str(file).split('.')[0]:
            ext = str(file).split('.')[1]
            source = FFmpegPCMAudio(f'Audio\{arg}.{ext}')
    player = voice.play(source)


@bot.command(pass_context = True)
async def chill(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Audio\supermarket.mp3')
        player = voice.play(source)
    else:
        await ctx.send('You are not connected to a voice channel for me to join!')




bot.run(BOTTOKEN)