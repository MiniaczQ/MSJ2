#	Parsing and interpreting discord input
from discordbot_init import *
from random import randint

@discordbot.event
async def on_message(message):
    global CHANNEL
    if not message.author.bot and message.channel.id == CHANNEL:
        content = message.content
        await message.delete()
        await discordbot.processCommand(content)

    else:
        content = message.content
        args = content.split()
        if len(args) > 1 and args[0] == "!stupify":
            string = "<@"+str(message.author.id) + "> says: "
            for i in content[9:]:
                string += "||"+i+"||"
            await message.channel.send(string)
        if len(args) == 1 and args[0] == "!findseed":
            eyes = 0
            for i in range(12):
                if randint(1,10) == 1:
                    eyes += 1
            await message.channel.send("<@"+str(message.author.id)+"> You got a "+str(eyes)+" eye.")
            


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
