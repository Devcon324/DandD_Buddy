from tkinter import N
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    # bot joins user's channel && Plays notification audio
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = str(self.bot.user).split("#").pop(0),
            description = "A D&D Bot designed to help Dungeon Master's and Players have a smooth online experience.\nMore features are yet to come",
            color = 0x00FFFF
            )
        embed.add_field(
            name = "Roll Dice",
            value = "Type '!roll' followed by the dice and optional modifier\n**Example**\n'!roll 1d20' = rolls 1 20-sided die\n'!roll 2d10 + 3' = rolls 2 10-sided dice and adds 3 once",
            inline = False
            )
        embed.add_field(
            name = "Battlemap Generator [Contributors Needed]",
            value = "Type '!battlemap [climate]' \n[climate] = 'forest' [more coming soon]\n**Example:**\n'!battlemap forest'",
            inline = False
            )
        embed.add_field(
            name = "Encounter Generator",
            value = "Generates an encounter following dndbeyond's algorithm https://www.dndbeyond.com/sources/basic-rules/building-combat-encounters\nType '!encounter [a] [b] [c] [d]' \n[a] = How Many Players?\n[b] = Player/party level\n[c] = How many monsters?\n[d] = Difficulty ('easy', 'medium', hard', 'deadly')\n**Example:**\n'!encounter 4 10 3 medium'",
            inline = False
            )
        embed.add_field(
            name = "Name Generator",
            value = "Generates 10 random names from the https://www.fantasynamegenerators.com\n**How to Use**\nType '!names'",
            inline = False
            )
        embed.add_field(
            name = "Voice Related Commands",
            value = "'!join' - joins your voice channel\n'!leave' - leaves your voice channel",
            inline = False
            )
        embed.add_field(
            name = "Music Related Commands",
            value = "'!play [Youtube URL]' - plays and queues music\n'!pause' - pauses current audio\n'!resume' - resumes current audio\n'!skip' - skips current audio\n'!stop' - stops & clears queue",
            inline = False
            )
        
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Help(bot))