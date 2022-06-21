import discord
import logging
from discord.ext import commands
import random
import requests
import json
import operator

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


class dice_roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, arg):
        
        if ctx.author == ctx.user:
            return
            
        # convert input to lwoercase for case-insensitivity
        input = str.lower(arg.content)
      
        # raw[1] = 1d20
        # raw[2] = + or -
        # raw[3] = modifier
        # dice[0] = # of dice
        # dice[1] = # of dice sides        
        name = str(ctx.author).rstrip("#123456789")
        roll_result = []
        total = 0
        raw = input.strip('!addroll').split(' ')
        dice = raw[1].split('d')
        
        for roll in range(int(dice[0])):
            roll = random.randint(1,int(dice[1]))
            roll_result.append(roll)
            total += roll        
        
        # list of the die rolls
        display_raw_roll = ["{}".format(roll_result)]
        
        # apply modifier once if present
        if len(raw) == 4:
            modifier = raw[3]
            total = ops[raw[2]](total, int(modifier))
            str_modifier = "{} {}".format(raw[2], raw[3])
            display_raw_roll = ["{} {}".format(roll_result, str_modifier)]
        
        # checks if result is longer than 2000char message & prints the final total
        x = len(str(roll_result))
        if x > 2000:
            await ctx.channel.send("Too many dice to handle!")
            return
        else:
            # shows user all dice rolls and modifier at end
            await ctx.channel.send(name + " Rolled: " + " {}".join(display_raw_roll))
            await ctx.channel.send(name + " Total: {}".format(total), tts=True)

        if int(dice[1]) == 20:
                natty_count = 0
                for number in roll_result:
                    if number == 20:
                        natty_count +=1
                if natty_count >= 2:
                    await ctx.channel.send("🎉 " + name + " Got {} Natural 20's!".format(natty_count), tts=True)
                elif natty_count == 1:
                    await ctx.channel.send("🎉 " + name + " Got a Natural 20!", tts=True)