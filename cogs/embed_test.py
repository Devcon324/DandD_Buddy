import discord
from discord.ext import commands

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
        Embed layout
        Concept = could use a JSON API of mosnter manual to take a command and provide an embed of a monster card
    """
    @commands.command()
    async def embed(self, ctx):
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
def setup(bot):
    bot.add_cog(Embed(bot))