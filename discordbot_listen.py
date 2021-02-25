class DiscordBotListen:
    async def on_message(self, message):
        if message.channel.id == self.CHANNEL and not message.author.bot:
            await message.delete()