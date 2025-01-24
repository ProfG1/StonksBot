import discord
from discord import app_commands
import os
from dotenv import load_dotenv

#for the token to not be leaked I put it in a separate file
load_dotenv(r"C:\Users\USER\Documents\DcBot\.env")
TOKEN: str = os.getenv("TOKEN")

# Initialize bot with appropriate intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = app_commands.CommandTree(client)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

@client.event
async def on_ready():
    await bot.sync(guild=discord.Object(id=1320393932378603644))
    print(f'Logged on as {client.user}!')


@bot.command(name="ping", description="Replies with pong and latency", guild=discord.Object(id=1320393932378603644))

async def ping(ctx: discord.Interaction):
    latency = round(client.latency * 1000)  # Convert latency to ms
    await ctx.response.send_message(f"Pong! Latency: {latency} ms")

# Run the bot
client.run(TOKEN)