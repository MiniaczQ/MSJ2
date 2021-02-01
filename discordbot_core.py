import os
import discord
from dotenv import load_dotenv

import discordbot_listener
import discordbot_reactor

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
discordbot = discord.Client()

@discordbot.event
async def on_ready():
    for guild in discordbot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{discordbot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@discordbot.event
async def on_message(message):
    if message.content == "!":
        response = f'Whats your command {message.author}?'
        await message.channel.send(response)

def discordbot_start():
    discordbot.start(TOKEN)