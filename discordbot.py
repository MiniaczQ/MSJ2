from os import getenv
from dotenv import load_dotenv
import discord
from discordbot_commands import DiscordBotCommands
from discordbot_react import DiscordBotReact
from discordbot_listen import DiscordBotListen


class DiscordBot(discord.Client, DiscordBotCommands, DiscordBotReact, DiscordBotListen):

    def __init__(self, manager, serverNames, channel, guild, serverSettings):
        self.CHANNEL = channel
        self.GUILD = guild
        discord.Client.__init__(self)
        self.manager = manager
        self.serverSettings = serverSettings
    
    async def on_ready(self):
        await self.setupCommands()
        channel = self.get_channel(self.CHANNEL)
        print(f"MSJ2 Discord Bot connected to #{channel.name} in {channel.guild.name}")
        await self.setupMessage()


if __name__ == "__main__":
    from manager import Manager
    from os import getcwd, path
    from logging_config import logging
    from unittest.mock import Mock
    root = getcwd()
    m = Manager(Mock(), logging, 12, root, path.join(root, 'templates'), 6, '192.168.1.2', 25566, path.join(root, 'servers'), path.join(root, 'worlds'), 'fabric-server-launch.jar')
    load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')
    CHANNEL = int(getenv('DISCORD_CHANNEL'))
    GUILD = int(getenv('DISCORD_GUILD'))
    a = DiscordBot(m, ["1","2","3"], CHANNEL, GUILD, serverSettings={
            "operator-mode": "auto",
            "version": "1.14.4",
            "whitelist-mode": "auto",
            "priority-mode": "message",
            "render-distance": 16
        })
    a.run(TOKEN)
