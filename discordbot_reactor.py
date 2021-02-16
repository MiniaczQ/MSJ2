#	Events that execute an action on discord
from discordbot_init import *


def checkPlayerName(playerName):
    '''
    Checks if a string can be an MC username
    '''
    # https://help.minecraft.net/hc/en-us/articles/360034636712-Minecraft-Usernames
    if len(playerName) < 3 or len(playerName) > 16:
        return False
    else:
        for i in playerName:
            if i not in "abcdefghijklmnopqrstuvwxyz"+"abcdefghijklmnopqrstuvwxyz".upper()+"0123456789_":
                return False
            return True


@discordbot.event
async def setupServerMessages(serverNames=["1", "2", "3"]):
    messages["servers"] = {}
    messages["control"] = {}

    channel = discordbot.get_channel(CHANNEL)

    for message in await channel.history(limit=1000).flatten():
        await message.delete()

    for serverName in serverNames:
        messages["servers"][serverName] = await channel.send(f"`World {serverName}` - 💤")

    messages["control"] = await channel.send("Click ❓ for a list of commands. Press ▶ to start the servers.")
    await messages["control"].add_reaction("❓")
    await messages["control"].add_reaction("▶")

    messages["response"] = await channel.send("```Waiting for command...```")


@discordbot.event
async def updateServerStatus(serverName, status):
    '''
    status can be set to:

    "D" for done (✅)

    "L" for loading (⌛)

    "S" for sleeping (💤)

    "R" for running (🏃)
    '''
    await messages["servers"][serverName].edit(content=f"`World {serverName}` - {STATUSDICT[status]}")


@discordbot.event
async def processCommand(content):
    global serverSettings
    args = str(content).split()
    if len(args) > 2:
        await discordbot.setResponse("Invalid command.")
    else:

        # OPERATOR-MODE

        if args[0] == "!opm":
            if len(args) == 1:
                await discordbot.setResponse(f"Operator mode is currently set to: {serverSettings['operator-mode']} ")
            else:
                if args[1] == "auto":
                    await discordbot.setResponse("Operator mode has been set to automatic.")
                    serverSettings['operator-mode'] = args[1]
                elif checkPlayerName(args[1]):
                    await discordbot.setResponse(f"Operator mode has been set to player '{args[1]}'.")
                    serverSettings['operator-mode'] = args[1]
                else:
                    await discordbot.setResponse(f"Invalid Player Name.")

        # VERSION

        elif args[0] == "!v":
            if len(args) == 1:
                await discordbot.setResponse(f"Version is currently set to: {serverSettings['version']} ")
            else:
                if args[1] in "1.7.2/1.14.4/1.15.2/1.15.2f/1.16.1/1.16.1f".split("/"):
                    await discordbot.setResponse(f"Version has been set to {args[1]}.")
                    serverSettings['version'] = args[1]
                else:
                    await discordbot.setResponse("Invalid version.")

        # WHITELIST-MODE

        elif args[0] == "!wlm":
            if len(args) == 1:
                await discordbot.setResponse(f"Whitelist mode is currently set to: {serverSettings['whitelist-mode']} ")
            else:
                if args[1] == "auto":
                    await discordbot.setResponse(f"Whitelist mode has been set to automatic.")
                    serverSettings['whitelist-mode'] = args[1]
                elif args[1] == "off":
                    await discordbot.setResponse(f"Whitelist mode has been set to off.")
                    serverSettings['whitelist-mode'] = args[1]
                else:
                    await discordbot.setResponse(f"Invalid whitelist mode.")

        # PRIORITY-MODE

        elif args[0] == "!pm":
            if len(args) == 1:
                await discordbot.setResponse(f"Priority mode is currently set to: {serverSettings['priority-mode']} ")
            else:
                if args[1] == "auto":
                    await discordbot.setResponse(f"Priority mode has been set to automatic.")
                    serverSettings['priority-mode'] = "auto"
                elif args[1] == "message":
                    await discordbot.setResponse(f"Priority mode has been set to message.")
                    serverSettings['priority-mode'] = "message"
                else:
                    await discordbot.setResponse(f"Invalid priority mode.")

        # INVALID

        else:
            await discordbot.setResponse("Invalid command.")
        
        #TODO: SEND serverSettings TO SERVER

        


@discordbot.event
async def swapState():
    await setRunning(not isRunning)


@discordbot.event
async def setResponse(content):
    await messages["response"].edit(content="```"+content+"```")


@discordbot.event
async def setRunning(value):
    global isRunning, messages
    if not value:
        # for serverName in list(messages["servers"]):
        #    await updateServerStatus(serverName, "S")
        await messages["control"].edit(content="Click ❓ for a list of commands. Press ▶ to start the servers.")
        await messages["control"].add_reaction("▶")
    else:
        # for serverName in list(messages["servers"]):
        #    await updateServerStatus(serverName, "L")
        await messages["control"].edit(content="Click ❓ for a list of commands. Press 🛑 to stop the servers.")
        await messages["control"].add_reaction("🛑")
    isRunning = value

    # send signal to servers
