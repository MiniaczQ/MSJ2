#	Events that execute an action on discord
from discordbot_init import discordbot, TOKEN, CHANNEL
from discordbot_core import serverMessages


async def setupServerMessages(serverNames=["1", "2", "3"]):
    for i in serverMessages:
        serverMessages.remove(i)

    channel = discordbot.get_channel(CHANNEL)

    for message in await channel.history(limit=1000).flatten():
        await message.delete()

    for serverName in serverNames:
        message = await channel.send(f"Server {serverName} - ⌛")
        serverMessages.append([serverName, message])


async def updateServerStatus(serverName, status):
    """
    status to be set to either True (meaning the server is loaded) or False (meaning the server is loading).
    status can also be a string for a custom status.
    """
    for i in serverMessages:
        if i[0] == serverName:
            if type(status) == type(True):
                if status:
                    status = "✅"
                else:
                    status = "⌛"
            await i[1].edit(content=f"Server {serverName} - {status}")
            break
