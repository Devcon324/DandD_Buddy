from platform import mac_ver
import discord
from discord.ext import commands
import json
import random


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

file = open('resources\monsters.json')
monster_manual = json.load(file)





players     = int(input("How Many Players?: "))
level       = int(input("What are their level?: "))
difficulty  = input("How Difficult is the fight?: ")
num_mons    = int(input("How Many Monsters?: "))


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
    print("Maximum XP Budget Range = ", lower_max_xp, " to ", upper_max_xp)

    # 
    lower_adj_max_xp = lower_max_xp / adjusted_xp_mod[num_mons]
    upper_adj_max_xp = upper_max_xp / adjusted_xp_mod[num_mons]
    print("Adjusted Maximum XP Budget Range = ", lower_adj_max_xp, " to ", upper_adj_max_xp)


mons_select = {}

count = 0
for i in monster_manual:
    
    a = str(i["Challenge"]).split(')')
    b = a[0].split("(").pop(1)
    xp = b.split(" ").pop(0).replace(",", "")
    
    if int(xp) <= upper_adj_max_xp:
        mons_select[i["name"]] = xp
        count += 1

for x, y in mons_select.items():
    print(x, y) 
        

print("*********************************************************")
print("")
print("")

viable_result = None
sum_xp = 0
#keys = random.sample(mons_select.items(), num_mons)
while viable_result == None:
    entry_list = list(mons_select.items())
    random_entry = random.sample(entry_list,  num_mons)
    for monster in random_entry:
        sum_xp += monster[1]
    if sum_xp > upper_adj_max_xp:
        viable_result = None
    else:
        viable_result = random_entry

print(viable_result)







file.close()




"""count = 0
for i in monster_manual:
    count += 1
    a = str(i["Challenge"]).split(')')
    b = a[0].split("(").pop(1)
    xp = b.split(" ").pop(0).replace(",", "")
    print(count, i["name"], xp)"""




























"""class Encounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #CODE GOES IN HERE

def setup(bot):
    bot.add_cog(Encounter(bot))"""