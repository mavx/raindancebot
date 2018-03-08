import os
import re

import requests
import discord
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
# DISCORD_WEBHOOK = os.getenv("DISCORD_RAINDANCE_WEBHOOK")
SLACK_WEBHOOK = os.getenv("SLACK_RAINDANCE_WEBHOOK")
TURTLE_ADDRESS = os.getenv("TURTLE_ADDRESS", "")
TURTLECOIN_SERVER_ID = '388915017187328002'
RAINDANCE_CHANNEL_ID = '407757902695235584'
TURTLERAINBOT_ID = '407753551859810304'

client = discord.Client()

async def notify(text):
    print("Notification message:", text)
    # if DISCORD_WEBHOOK:
    #     print("Notifying Discord..")
    #     requests.post(DISCORD_WEBHOOK, json={"content": text})
    
    if SLACK_WEBHOOK:
        print("Notifying Slack..")
        requests.post(SLACK_WEBHOOK, json={"text": text})

# def extract_title(message):
#     return message.embeds[0].get('title', '').lower()

# def extract_description(message):
#     return message.embeds[0].get('description', '').lower()

def message_contains(message, condition):
    conditions = {
        'tut_tut': 'tut tut',
        'raining': "it's raining",
        'send_address': "send me your wallet address",
        'react': ''
    }
    print("Scanning for:", conditions.get(condition, 'N/A'))
    print("Message to scan: {}".format(str(message.embeds).lower())
    return conditions.get(condition, 'N/A') in str(message.embeds).lower()

def print_message(message):
    print("TurtleMessage:", message.content)
    print("Author:", message.author)
    print("Embeds:", message.embeds)
    print("ID:", message.id)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('______')

@client.event
async def on_message(message):
    if (message.channel.id != RAINDANCE_CHANNEL_ID) or (message.author.id != TURTLERAINBOT_ID):
        return
    elif not message.embeds: # Check for attachments
        return
    
    emoji_list = message.server.emojis

    print_message(message)
    print("Emojis:", emoji_list)

    # Check for rain    
    if not message_contains(message, 'tut_tut'):
        return
    
    # OK, it's gonna rain
    await notify("It's gonna rain!")

    # Wait for it to rain
    raining = False
    print("Raining:", raining)
    while not raining:
        print("Checking in 5 seconds...")
        await asyncio.sleep(5)
        async for log in client.logs_from(message.channel, limit=2, reverse=True):
            if message_contains(log, 'raining') and (log.author == message.author):
                raining = True
                await notify("It's raining!")
                print_message(log)
    print("Raining:", raining)

    # Wait for the cue to send address
    address_requested = False
    print("Address requested:", address_requested)
    while not address_requested:
        print("Checking in 10 seconds...")
        await asyncio.sleep(10)
        async for log in client.logs_from(message.channel, limit=2, reverse=True):
            if message_contains(log, 'send_address') and (log.author == message.author):
                address_requested = True
                await notify("Sending your address!")
                await client.send_message(message.author, TURTLE_ADDRESS)
                print_message(log)
    print("Address requested:", address_requested)

    # Wait for reaction
    print("Waiting for reaction...")
    private_message = await client.wait_for_message(timeout=15, author=message.author)
    print_message(private_message)
    regex = re.search(r"<\S{22,}>", message.content)
    if regex is not None:
        for emoji in elist:
            if str(emoji) == regex.group(0):
                await notify("Reacting to the rain lol.")
                await bot.add_reaction(rain_message, emoji)
    else:
        notify("Emoji not found, GG.")


client.run(TOKEN, bot=False)
