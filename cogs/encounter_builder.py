from platform import mac_ver
import discord
from discord.ext import commands
import json
import random
import asyncio
from numpy import imag
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


xp_thresholds = {
# Level:   [Easy, Medium, Hard, Deadly],
    1: [25, 50, 75, 100],
    2: [50, 100, 150, 200],
    3: [75, 150, 225, 400],
    4: [125, 250, 375, 500],
    5: [250, 500, 750, 1100],
    6: [300, 600, 900, 1400],
    7: [350, 750, 1100, 1700],
    8: [450, 900, 1400, 2100],
    9: [550, 1100, 1600, 2400],
    10: [600, 1200, 1900, 2800],
    11: [800, 1600, 2400, 3600],
    12: [1000, 2000, 3000, 4500],
    13: [1100, 2200, 3400, 5100],
    14: [1250, 2500, 3800, 5700],
    15: [1400, 2800, 4300, 6400],
    16: [1600, 3200, 4800, 7200],
    17: [2000, 3900, 5900, 8800],
    18: [2100, 4200, 6300, 9500],
    19: [2400, 4900, 7300, 10900],
    20: [2800, 5700, 8500, 12700],
}

diff_dict = {
    'easy': 0,
    'medium': 1,
    'hard': 2,
    'deadly': 3
}

adjusted_xp_mod = {
# Numofmonsters : countP Multiplier
    1: 1.0,
    2: 1.5,
    3: 2.0,
    4: 2.0,
    5: 2.0,
    6: 2.0,
    7: 2.5,
    8: 2.5,
    9: 2.5,
    10: 2.5,
    11: 3.0,
    12: 3.0,
    13: 3.0,
    14: 3.0,
    15: 4.0
}





class EncounterGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def encounter(self, message, *args):
        if message.author == self.bot.user:
            return
        if len(args) == 0:
            embed = discord.Embed(
                title="D&D Encounter Generator",
                description="Type !encounter [a] [b] [c] [d] \n[a] = How Many Players?\n[b] = Player/party level\n[c] = How many monsters?\n[d] = Difficulty ('easy', 'medium', hard', 'deadly')\n"
            )
            await message.send(embed=embed)
        else:
            players     = int(args[0])
            level       = int(args[1])
            num_mons    = int(args[2])
            difficulty  = str(args[3])

            print("----------------------------------------")
            print("Players    = ", players)
            print("Level      = ", level)
            print("Num-Mons   = ", num_mons)
            print("Difficulty = ", difficulty)
            print("----------------------------------------")

            file = open('resources\monsters.json')
            monster_manual = json.load(file)
            diff = None

            # check if the level is in the xp threshold table
            if level in xp_thresholds.keys():
                # find the max XP requriements for the requested difficulty
                if difficulty in diff_dict.keys():
                    diff = diff_dict[difficulty]
                    print("diff = ", diff)
                

                #this is the maximum XP needed for the requested difficulty
                lower_max_xp = players * xp_thresholds[level][diff]
                upper_max_xp = players * xp_thresholds[level][diff+1]
                print("Maximum XP Budget Range          = ", lower_max_xp, " to ", upper_max_xp)

                # 
                lower_adj_max_xp = lower_max_xp / adjusted_xp_mod[num_mons]
                upper_adj_max_xp = upper_max_xp / adjusted_xp_mod[num_mons]
                print("Maximum XP Budget Range Adjusted = ", lower_adj_max_xp, " to ", upper_adj_max_xp)

            
            mons_select = {}
            """
            {
                "name" : [xp, ac, hp, speed, image]
            }
            """

            count = 0
            for i in monster_manual:
                

                a = str(i["Challenge"]).split(')')
                b = a[0].split("(").pop(1)

                # gives an int without comma of the xp value
                xp = b.split(" ").pop(0).replace(",", "")
                
                # creacts a dict of key-value pairts of name - traits

                # slices off the monsters who have a individual xp higher than the max
                if int(xp) <= upper_adj_max_xp:
                    mons_traits = []
                    mons_traits.append(xp)
                    mons_traits.append(i["Armor Class"])
                    mons_traits.append(str(i["Hit Points"]).split(" ").pop(0))
                    mons_traits.append(i["Speed"])
                    mons_traits.append(i["img_url"])
                    mons_traits.append(i["Challenge"])
                    
                    mon_name = i["name"]
                    mons_select[mon_name] = mons_traits

                    """
                    print(mons_traits)
                    mons_select[i["name"]].append(mons_traits)"""
                    count += 1


            """for x, y in mons_select.items():
                print(x, y) """
                    

            print("*********************************************************")
            
            while True:
                sum_xp = 0
                entry_list = list(mons_select.items())
                random_entry = random.sample(entry_list, num_mons)
                #print("*********************************************************")
                #print(random_entry)

                for monster in random_entry:
                    #print(f"the xp for {monster[0]} = {monster[1][0]}")
                    sum_xp += int(monster[1][0])

                #print(sum_xp)
                if sum_xp >= lower_adj_max_xp and sum_xp <= upper_adj_max_xp:
                    break

            print("*********************************************************")
            images = []
            for monster in random_entry:
                print(f"{monster}")
                print(f"the xp for {monster[0]} = {monster[1][0]}")
                images.append(monster[1][4])
            print(f"summed xp = {sum_xp}")
            
            thumbnail_url = str(random.choice(images))

            embed = discord.Embed(
                title = "Your Random Generated Encounter!", 
                description = f"This is a **{difficulty} difficulty** encounter for **{players} players**, at **level {level}**.\nClick links for more information and images",
                color = 0x00FFFF
                )
            embed.set_image(
                url=thumbnail_url
            )
            for mon in random_entry:
                embed.add_field(
                    name = f"{mon[0]}",
                    value = f"CR = {mon[1][5]}\nAC = {mon[1][1]}\nHP = {mon[1][2]}\nSpeed = {mon[1][3]}\nhttps://www.aidedd.org/dnd/monstres.php?vo={mon[0].replace(' ', '-')}",
                    inline = True
                    )
            embed.set_footer(
            text = "Encounter generated following dndbeyond's algorithm\nhttps://www.dndbeyond.com/sources/basic-rules/building-combat-encounters"
            )
            
            await message.send(embed=embed)

            file.close()

def setup(bot):
    bot.add_cog(EncounterGenerator(bot))

