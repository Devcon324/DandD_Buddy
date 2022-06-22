import discord
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
import random
import operator
import os
import asyncio
import youtube_dl
import time
from titlecard import titlecard
from apikeys import *

#setup
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.xor,
}
client = discord.Client()
bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
    titlecard(bot)

@bot.command()
async def hello(ctx):
    greetings = [
        'Hey',
        'Hello',
        'Wassup',
        'Hi',
        'Bonjour',
        'Hello there, ']
    await ctx.channel.send(f"{random.choice(greetings)} {str(ctx.author).split('#')[0]} I am {bot.user}")

# takes !roll argument, case insensitive
# Examples: "!roll 1d20", "!roll 1d20 + 5"
@bot.command()
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
@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Audio\kill-kill.mp3')
        voice.play(source)
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


bot.run(BOTTOKEN)