from discord_slash.utils import manage_commands

class DiscordBotReact:
    async def setupMessage(self):
        self.get_channel(self.CHANNEL)
        channel = self.get_channel(self.CHANNEL)
        for message in await channel.history(limit=1000).flatten():
            await message.delete()

        self.message = await channel.send(content="L")
        await self.updateMessage()

    async def updateMessage(self):
        worlds = ""
        await self.message.edit(content=f'''
        Worlds:
        {worlds}
        Game Settings:```
        Render Distance: {self.serverSettings['render-distance']}
        Game Version: {self.getTemplateName(self.serverSettings['version'])}
        Whitelist Mode: {self.serverSettings['whitelist-mode']}
        Priority Mode: {self.serverSettings['priority-mode']}
        Operator Mode: {self.serverSettings['operator-mode']}
        ```'''.replace("    ", "")
        )
    
    def getWorldsString(self):
        worlds = ""
        for i in self.manager.servers:
            i.state()

    def getTemplateName(self,name):
        if name[-1] == "f":
            name = name[:-1] + " with Fabric"
        else:
            name += " Vanilla"
        return name

    async def updateTemplates(self):
        choices = []
        for i in self.manager.get_all_templates():
            choices.append(
                manage_commands.create_choice(i, self.getTemplateName(i))
            )
        self.slash.commands['version'].options = [
            manage_commands.create_option(
                "version",
                "The game version to set the juggler to.",
                3,
                True,
                choices=choices
            )
        ]
