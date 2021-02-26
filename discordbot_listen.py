import discord_slash
from discord_slash.utils import manage_commands


class DiscordBotListen:

    async def on_message(self, message):
        if message.channel.id == self.CHANNEL and not message.author.bot:
            await message.delete()

    async def setupCommands(self):
        self.slash = discord_slash.SlashCommand(self, True)

        @self.slash.slash(
            name="render-distance",
            description="Change render distance.",
            guild_ids=[self.GUILD],
            options=[
                manage_commands.create_option(
                    "amount",
                    "The render distance to set the juggler's worlds to.",
                    4,
                    True
                )
            ]
        )
        async def commandRD(ctx, amount: int):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                amount = max(2, min(amount, 32))
                self.serverSettings["render-distance"] = amount
                self.hasChanges = True
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="version",
            description="Change game version.",
            guild_ids=[self.GUILD]
        )
        async def commandVersion(ctx, version: str):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL and version in self.manager.get_all_templates():
                self.serverSettings["version"] = version
                self.hasChanges = True
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="whitelist-mode",
            description="Change whitelist mode.",
            guild_ids=[self.GUILD],
            options=[
                manage_commands.create_option(
                    "mode",
                    "The whitelist mode.",
                    3,
                    True,
                    choices=[
                        manage_commands.create_choice("auto", "Automatic"),
                        manage_commands.create_choice("off", "Off")
                    ]
                )
            ]
        )
        async def commandWLM(ctx, mode: str):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                self.serverSettings["whitelist-mode"] = mode
                self.hasChanges = True
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="operator-mode",
            description="Change operator mode.",
            guild_ids=[self.GUILD],
            options=[
                manage_commands.create_option(
                    "player", "The player to set operator mode to (or 'auto' for automatic).", 3, True)
            ]
        )
        async def commandOPM(ctx, player):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                self.serverSettings["operator-mode"] = player
                self.hasChanges = True
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="priority-mode",
            description="Change priority mode.",
            guild_ids=[self.GUILD],
            options=[
                manage_commands.create_option(
                    "mode",
                    "The mode to set priority mode to.",
                    3,
                    True,
                    choices=[
                        manage_commands.create_choice(
                            "message", "On Operator Message"),
                        manage_commands.create_choice(
                            "2player", "On Second Player Join")
                    ]
                )
            ]
        )
        async def commandPM(ctx, mode):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                self.serverSettings["priority-mode"] = mode
                self.hasChanges = True
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="start",
            description="Starts/Restarts the servers. This will also load the settings.",
            guild_ids=[self.GUILD]
        )
        async def commandStart(ctx):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                # TODO:Apply settings to manager
                # TODO:Stop then start manager
                self.hasChanges = False
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="stop",
            description="Stops the servers. This will also load the settings.",
            guild_ids=[self.GUILD]
        )
        async def commandStop(ctx):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                # TODO:Stop manager
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="reload",
            description="Reload juggler stuff for the discord bot and apply settings.",
            guild_ids=[self.GUILD]
        )
        async def commandReload(ctx):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                # TODO:Apply settings to manager
                self.hasChanges = False
                await self.updateTemplates()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        await self.updateTemplates()
