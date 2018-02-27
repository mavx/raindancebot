import discord
import asyncio
import os

client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('______')

@client.event
async def on_message(message):
    if message.server.name.lower() != 'mouland':
        return

    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            print(log.content)
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    
    elif message.content.startswith('$'):
        print("Message:", message.content)
        # await client.send_message(message.channel, "Yep got it")
        channel = client.get_channel('407757902695235584')
        async for tm in client.logs_from(channel, limit=2, reverse=True):
            print("TurtleMessage:", tm.content)
            print("Author:", tm.author)
            print("Attachments:", tm.attachments)
            print("ID:", tm.id)
            print("Timestamp:", tm.timestamp)
            print("Edited:", tm.edited_timestamp)
            print("Type:", tm.type)
            print("SystemContent:", tm.system_content)
            print("Embeds:", tm.embeds)
    

client.run(TOKEN, bot=False)
