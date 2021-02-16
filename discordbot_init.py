from os import getenv
import discord
from dotenv import load_dotenv

messages = {"servers": {}, "control": None, "response": None}
isRunning = False
inARun = False
serverNamesStart = []
alreadyStarted = False
STATUSDICT = {
    "Done": "✅",
    "Loading": "⌛",
    "Sleeping": "💤",
    "Running": "🏃‍♂️",
    "D": "✅",
    "L": "⌛",
    "S": "💤",
    "R": "🏃‍♂️",
    "✅": "✅",
    "⌛": "⌛",
    "💤": "💤",
    "🏃‍♂️": "🏃‍♂️"
}
helpMessage = """--------------------------------



**__Server Juggler Commands__**

Use these commands in the #server-status channel.
Run the commands without the option to get their current setting.

Change Operator Mode:
`!opm [auto/(playername)]`
`auto` - The first player to join the server will receive operator.
`(playername)` - Replace with a player's in game name 

Change Version:
`!v [1.7.2/1.14.4/1.15.2/1.15.2f/1.16.1/1.16.1f]`
Versions with `f` on the end mean fabric with lithium/phosphor (allowed on speedrun.com).

Change Whitelist Mode:
`!wlm [auto/off]`
`auto` - Anyone can join the server before the run starts and is added to the whitelist. The whitelist is then turned on once the run starts.
`off` - Servers will start with whitelist off and empty, allowing anyone to join at any time.

Change Priority Mode:
`!pm [2player/message]`
`2player` - If a second player joins the server, it will enable priority on the world.
`message` - If a player sends a message in the chat, it will enable priority on the world.

"""

serverSettings = {
    "operator-mode": "auto",
    "version": "1.14.4",
    "whitelist-mode": "auto",
    "priority-mode": "message"
}

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
CHANNEL = int(getenv('DISCORD_CHANNEL'))

discordbot = discord.Client()
