import discord
import logging
from discord.ext import commands
import random
import requests
import json


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



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

    if input.startswith('!roll'):
        dice = input.strip('!roll ').split('d')
        result = []
        for roll in range(int(dice[0])):
            roll = random.randint(1,int(dice[1]))
            result.append(roll)

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