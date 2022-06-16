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

# Since the on_message() event triggers for every message received, we have to make sure that we ignore messages from ourselves. 
# We do this by checking if the Message.author is the same as the Client.user.
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
    if input.startswith('!roll'):
        raw = input.strip('!roll').split(' ')
        await message.channel.send(raw)
        dice = raw[1].split('d')
        await message.channel.send(dice)
        modifier = raw[3]
        result = []

        for roll in range(int(dice[0])):
            roll = random.randint(1,int(dice[1]))
            roll_mod = ops[raw[2]](roll, int(modifier)) 
            result.append(roll_mod)
            await message.channel.send(roll)
            await message.channel.send(roll_mod)

        x = len(str(result))
        if x > 2000:
            await message.channel.send("Too many dice to handle!")
            return

        await message.channel.send(result)
        if int(dice[1]) == 20:
            natty_count = 0
            for number in result:
                if number == 20:
                    natty_count +=1
            if natty_count >= 2:
                await message.channel.send("🎉 That's {} Natural 20's! 🎉".format(natty_count))
            elif natty_count == 1:
                await message.channel.send("🎉 That's a Natural 20! 🎉")

    











client.run('OTg2ODMzOTU1NTMxNjUzMTUw.Gma0XO.7cVBa6U6VhKMgwp-Zssm3EjYk9x96GSxZrMSNg')