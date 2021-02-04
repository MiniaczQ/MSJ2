from discordbot_init import *
import discordbot_listener
import discordbot_reactor

@discordbot.event
async def on_ready():
    global serverNamesStart
    channel = discordbot.get_channel(CHANNEL)
    guild = channel.guild
    
    print(f"MSJ2 Discord Bot connected to #{channel.name} in {guild.name}")

    if len (serverNamesStart) > 0:
        await discordbot.setupServerMessages(serverNamesStart)

def discordbot_start(serverNames=[]):
    global serverNamesStart
    serverNamesStart = serverNames
    discordbot.run(TOKEN)

if __name__ == "__main__":
    discordbot_start()