from discordbot_init import discordbot, TOKEN, CHANNEL
import discordbot_listener
import discordbot_reactor

serverMessages = []



@discordbot.event
async def on_ready():
    channel = discordbot.get_channel(CHANNEL)
    guild = channel.guild
    
    print(f"MSJ2 Discord Bot connected to #{channel.name} in {guild.name}")

    if __name__ == "__main__":
        import time
        await discordbot_reactor.setupServerMessages()
        time.sleep(5)
        await discordbot_reactor.updateServerStatus("3",True)
        time.sleep(5)
        await discordbot_reactor.updateServerStatus("1",True)
        time.sleep(5)
        await discordbot_reactor.updateServerStatus("2",True)

def discordbot_start():
    discordbot.run(TOKEN)

if __name__ == "__main__":
    discordbot_start()