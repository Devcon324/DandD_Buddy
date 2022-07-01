import discord
from discord.ext import commands

class ErrorCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
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
def setup(bot):
    bot.add_cog(ErrorCheck(bot))