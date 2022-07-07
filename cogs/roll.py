import discord
from discord.ext import commands
import random
import operator
ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
    '%' : operator.mod,
    '^' : operator.xor,
}

# user can roll dice with/without modifiers
"""
    Add a boolean variable that saves True or false to a global variable of TTS
    This allows for users to toggle TTS On/Off for the bot
"""
class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def roll(self, ctx, *args):
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

def setup(bot):
    bot.add_cog(Roll(bot))