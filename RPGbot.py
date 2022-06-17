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

client = discord.Client()

# This is to learn API Linking for D&D API linkage for Rule calls
sad_words = [
    "sad", 
    "depressed", 
    "unhappy"
    ]
starter = [
    "Cheer up!",
    "Hang in there!"
]
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # convert input to lwoercase for case-insensitivity
    input = str.lower(message.content)
    # this code block will reply with a quote
    if input.startswith('!hello'):
        quote = get_quote()
        await message.channel.send(quote)
    # this code will scan for key words and reply with random phrase
    if any(word in input for word in sad_words):
        await message.channel.send(random.choice(starter))

# raw[1] = 1d20
# raw[2] = + or -
# raw[3] = modifier
# dice[0] = # of dice
# dice[1] = # of dice sides
    if input.startswith('!roll'):
        name = str(message.author).rstrip("#123456789")
        result = []
        total = 0
        raw = input.strip('!addroll').split(' ')
        dice = raw[1].split('d')
        
        for roll in range(int(dice[0])):
            roll = random.randint(1,int(dice[1]))
            result.append(roll)
            total += roll        
        
        # list of the die rolls
        display_raw_roll = ["{}".format(result)]
        
        # apply modifier once if present
        if len(raw) == 4:
            modifier = raw[3]
            total = ops[raw[2]](total, int(modifier))
            str_modifier = "{} {}".format(raw[2], raw[3])
            display_raw_roll = ["{} {}".format(result, str_modifier)]
        
        # checks if result is longer than 2000char message & prints the final total
        x = len(str(result))
        if x > 2000:
            await message.channel.send("Too many dice to handle!")
            return
        else:
            # shows user all dice rolls and modifier at end
            await message.channel.send(name + " Rolled: " + " {}".join(display_raw_roll))
            await message.channel.send(name + " Total: {}".format(total), tts=True)

    if int(dice[1]) == 20:
            natty_count = 0
            for number in result:
                if number == 20:
                    natty_count +=1
            if natty_count >= 2:
                await message.channel.send("🎉 " + name + " Got {} Natural 20's!".format(natty_count), tts=True)
            elif natty_count == 1:
                await message.channel.send("🎉 " + name + " Got a Natural 20!", tts=True)








client.run('OTg2ODMzOTU1NTMxNjUzMTUw.Gma0XO.7cVBa6U6VhKMgwp-Zssm3EjYk9x96GSxZrMSNg')