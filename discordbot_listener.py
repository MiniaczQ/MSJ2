#	Parsing and interpreting discord input
from discordbot_init import *


@discordbot.event
async def on_message(message):
    global CHANNEL
    if not message.author.bot and message.channel.id == CHANNEL:
        content = message.content
        await message.delete()
        await discordbot.processCommand(content)


@discordbot.event
async def on_reaction_add(reaction, user):
    global helpMessage, CHANNEL
    message = reaction.message
    if not user.bot:
        if message.channel.id == CHANNEL:
            await reaction.remove(user)
        if message.id == messages["control"].id:
            if reaction.emoji in ["▶", "🛑"]:
                await reaction.remove(discordbot.user)
                await discordbot.swapState()
            elif reaction.emoji == "❓":
                await user.send(helpMessage)
