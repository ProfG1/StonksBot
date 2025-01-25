import discord
from discord import app_commands

class Command: # Base class for all commands
    def __init__(self, name: str, description: str, guild: discord.Object): 
        self.name = name
        self.description = description
        self.guild = guild

    async def invoke(self, ctx: discord.Interaction): # Method to be overridden by subclasses
        raise NotImplementedError

class PingCommand: 
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int): # Initialize the command
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self): # Register the command
        @self.bot.command(name="ping", description="Replies with pong and latency", guild=discord.Object(id=self.guild_id))
        async def ping(ctx: discord.Interaction):
            latency = round(self.client.latency * 1000)  # Convert latency to ms
            await ctx.response.send_message(f"Pong! Latency: {latency} ms")