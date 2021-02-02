from discordbot_init import discordbot, TOKEN, CHANNEL, messages, isRunning, serverNamesStart
import discordbot_listener
import discordbot_reactor

@discordbot.event
async def on_ready():
    global serverNamesStart
    channel = discordbot.get_channel(CHANNEL)
    guild = channel.guild
    
    print(f"MSJ2 Discord Bot connected to #{channel.name} in {guild.name}")

    discordbot_reactor.setupServerMessages(serverNamesStart)
def start(serverNames=["1","2","3"]):
    global serverNamesStart
    discordbot.run(TOKEN)
    serverNamesStart = serverNames

if __name__ == "__main__":
    start()