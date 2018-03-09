import os
import re
import logging

import requests
import discord
import asyncio

logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%m-%d %H:%M',
    filename='raindance.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("DISCORD_TOKEN")
# DISCORD_WEBHOOK = os.getenv("DISCORD_RAINDANCE_WEBHOOK")
SLACK_WEBHOOK = os.getenv("SLACK_RAINDANCE_WEBHOOK")
TURTLE_ADDRESS = os.getenv("TURTLE_ADDRESS", "")
TURTLECOIN_SERVER_ID = '388915017187328002'
RAINDANCE_CHANNEL_ID = '407757902695235584'
TURTLERAINBOT_ID = '407753551859810304'

client = discord.Client()


async def notify(text):
    logger.debug("Notification message: {}".format(text))
    # if DISCORD_WEBHOOK:
    #     logger.info("Notifying Discord..")
    #     requests.post(DISCORD_WEBHOOK, json={"content": text})

    if SLACK_WEBHOOK:
        logger.info("Notifying Slack..")
        requests.post(SLACK_WEBHOOK, json={"text": text})


def message_contains(message, condition):
    conditions = {
        'tut_tut': 'tut tut',
        'raining': "it begins to rain",
        'send_address': "send me your wallet address",
        'react': ''
    }
    logger.info("Scanning for: {}".format(conditions.get(condition, 'N/A')))
    logger.info("Message to scan: {}".format(str(message.embeds).lower()))
    return conditions.get(condition, 'N/A') in str(message.embeds).lower()


def print_message(message):
    logger.debug("TurtleMessage: {}".format(message.content))
    logger.debug("Author: {}".format(message.author))
    logger.debug("Embeds: {}".format(message.embeds))
    logger.debug("ID: {}".format(message.id))


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
    elif not message.embeds:  # Check for attachments
        return

    emoji_list = message.server.emojis

    print_message(message)
    logger.debug("Emojis: {}".format(map(str, emoji_list)))

    # Check for rain    
    if not message_contains(message, 'tut_tut'):
        return

    # OK, it's gonna rain
    await notify("It's gonna rain!")

    # Wait for it to rain
    raining = False
    logger.debug("Raining: {}".format(raining))
    while not raining:
        logger.info("Checking in 5 seconds...")
        await asyncio.sleep(5)
        async for log in client.logs_from(message.channel, limit=2, reverse=True):
            if message_contains(log, 'raining') and (log.author == message.author):
                raining = True
                await notify("It's raining!")
                print_message(log)
    logger.debug("Raining: {}".format(raining))

    # Wait for the cue to send address
    address_requested = False
    logger.debug("Address requested: {}".format(address_requested))
    while not address_requested:
        logger.info("Checking in 10 seconds...")
        await asyncio.sleep(10)
        async for log in client.logs_from(message.channel, limit=2, reverse=True):
            if message_contains(log, 'send_address') and (log.author == message.author):
                address_requested = True
                await notify("Sending your address!")
                await client.send_message(message.author, TURTLE_ADDRESS)
                print_message(log)
    logger.debug("Address requested: {}".format(address_requested))

    # Wait for reaction
    logger.info("Waiting for reaction...")
    private_message = await client.wait_for_message(timeout=15, author=message.author)
    print_message(private_message)
    regex = re.search(r"<\S{22,}>", private_message.content)
    if regex is not None:
        for emoji in emoji_list:
            if str(emoji) == regex.group(0):
                await notify("Reacting to the rain lol.")
                await client.add_reaction(message, emoji)
    else:
        await notify("Emoji not found, GG.")


client.run(TOKEN, bot=False)
