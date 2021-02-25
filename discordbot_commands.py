import discord_slash
from discord_slash.utils import manage_commands


class DiscordBotCommands:

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
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        @self.slash.slash(
            name="reload",
            description="Reload juggler stuff for the discord bot.",
            guild_ids=[self.GUILD]
        )
        async def commandReload(ctx):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                await self.updateTemplates()
                await self.slash.sync_all_commands()
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
                    "wlm",
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
        async def commandWLM(ctx, wlm: str):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                self.serverSettings["whitelist-mode"] = wlm
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
        async def commandOPM(ctx, mode):
            await ctx.respond()
            if ctx.message.channel.id == self.CHANNEL:
                self.serverSettings["priority-mode"] = mode
                await self.updateMessage()
            else:
                await ctx.send(f"{ctx.message.author.mention} Please use the <#{str(self.CHANNEL)}> channel!")
                await ctx.message.delete()

        await self.updateTemplates()
