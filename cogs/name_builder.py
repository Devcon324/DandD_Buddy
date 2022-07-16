from tkinter import N
import discord
from discord.ext import commands
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NameGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def names(self, message):
        if message.author == self.bot.user:
            return

        URL = "https://www.fantasynamegenerators.com/hobbit-names.php"
        driver = webdriver.Chrome("tools/chromedriver.exe")
        driver.get(URL)
        driver.implicitly_wait(10)
        result = driver.find_element(by=By.ID, value="result")
        name_string = result.text
        #names = name_string.split("\n")
        driver.quit()
        
        embed = discord.Embed(
            title = "Fantasy Name Generator", 
            url = "https://www.fantasynamegenerators.com",
            color = 0x00FFFF
            )
        embed.add_field(
            name = "Random Names",
            value = name_string,
            inline = False
            )
        embed.set_footer(
            text = "Source: https://www.fantasynamegenerators.com"
            )
        
        await message.send(embed=embed)

        guild_name = message.message.guild.name
        guild_ID = message.message.guild.id
        print(f"***************************\nRequest for Name Generation to {URL}\nServer Name: {guild_name}\nGuild ID: {guild_ID}\n***************************")
        

def setup(bot):
    bot.add_cog(NameGenerator(bot))