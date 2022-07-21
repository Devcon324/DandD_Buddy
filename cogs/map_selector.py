import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import random


class battlemap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    # bot joins user's channel && Plays notification audio
    @commands.command()
    async def battlemap(self, ctx, *args):
        # !battlemap forest
        climate = str.lower(args[0])
        path = f"images\\battlemaps\\{climate}"
        battlemap_list = []

        for battlemap in os.listdir(path):
            battlemap_list.append(os.path.join(path, battlemap))
        random_map = random.choice(battlemap_list)

        await ctx.channel.send(file=discord.File(random_map))

def setup(bot):
    bot.add_cog(battlemap(bot))