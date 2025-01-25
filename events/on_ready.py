import discord
from discord import app_commands

class OnReadyEvent:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def on_ready(self):
        await self.bot.sync(guild=discord.Object(id=self.guild_id))
        print(f'Logged on as {self.client.user}!')
