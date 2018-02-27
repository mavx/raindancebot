import os

import requests
import discord
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK = os.getenv("DISCORD_RAINDANCE_WEBHOOK")
SERVER_LIST = ['turtlecoin']

client = discord.Client()

def is_targeted_message(message):
    return any(server in message.server.name.lower() for server in SERVER_LIST)

def notify(text):
    print(text)
    return requests.post(WEBHOOK, json={"content": text})

def extract_description(message):
    return message.embeds[0].get('description', '')

def message_contains(message, condition):
    conditions = {
        'tut_tut': 'tut tut',
        'raining': "it's raining",
        'send_address': "send me your wallet address",
        'react': ''
    }
    return conditions.get(condition, '') in extract_description(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('______')

@client.event
async def on_message(message):
    # Ignore PMs and messages on other servers
    if message.server is None:
        print("PM:", message)
        return
    elif not is_targeted_message(message):
        return

    # Check for rain
    if 'turtlecoin' in message.server.name.lower():
        if message.embeds:
            if message_contains(message, 'tut_tut'):
                notify("It's gonna rain!")

                # Wait for it to rain
                await asyncio.sleep(10)
                async for log in client.logs_from(message.channel, author=message.author, limit=5, reverse=True):
                    if message_contains(message, 'raining'):
                        notify("It's raining!")

                # Wait for the cue to send address
                await asyncio.sleep(10)
                async for log in client.logs_from(message.channel, author=message.author, limit=5, reverse=True):
                    if message_contains(message, 'send_address'):
                        notify("Alright, time to send your address!")

                # Wait for reaction

                notify("Reacting to the rain lol.")


    # if message.content.startswith('!test'):
    #     counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         print(log.content)
    #         if log.author == message.author:
    #             counter += 1

    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')
    
    # elif message.content.startswith('$'):
    #     print("Message:", message.content)
    #     # await client.send_message(message.channel, "Yep got it")
    #     channel = client.get_channel('407757902695235584')
    #     async for tm in client.logs_from(channel, limit=2, reverse=True):
    #         print("TurtleMessage:", tm.content)
    #         print("Author:", tm.author)
    #         print("Attachments:", tm.attachments)
    #         print("ID:", tm.id)
    #         print("Timestamp:", tm.timestamp)
    #         print("Edited:", tm.edited_timestamp)
    #         print("Type:", tm.type)
    #         print("SystemContent:", tm.system_content)
    #         print("Embeds:", tm.embeds)
    

client.run(TOKEN, bot=False)
