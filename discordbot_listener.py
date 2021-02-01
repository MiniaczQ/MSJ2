#	Parsing and interpreting discord input
from discordbot_init import discordbot, TOKEN, CHANNEL
import discordbot_reactor

@discordbot.event
async def on_message(message):
    if "showonthebotplease" in message.content:
        print(message.content)

@discordbot.event
async def on_reaction_add(reaction, user):
    print(reaction.message)