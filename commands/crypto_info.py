import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import os
import asyncio
from dotenv import load_dotenv
from utils.fetch_data import get_crypto_info

class CryptoInfoCommand:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self):
        @self.bot.command(name="crypto_info", description="Get cryptocurrency information", guild=discord.Object(id=self.guild_id))
        async def crypto_info(ctx: discord.Interaction, crypto_id: str):
            load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
            api_key = os.getenv("CRYPTO")

            data = get_crypto_info(crypto_id, api_key)
            if not data:
                await ctx.response.send_message("Invalid cryptocurrency ID.")
                return

            # Create an embed with the cryptocurrency information
            embed = discord.Embed(title="Cryptocurrency Information", color=discord.Color.gold())
            embed.set_thumbnail(url=data['image']['large'])
            embed.add_field(name="Symbol", value=data['symbol'].upper(), inline=False)
            embed.add_field(name="Name", value=data['name'], inline=False)
            embed.add_field(name="Current Price", value=f"${data['market_data']['current_price']['usd']:,.2f}", inline=False)
            embed.add_field(name="24-Hour Change", value=f"{data['market_data']['price_change_percentage_24h']:+.2f}%", inline=False)
            embed.add_field(name="Market Cap", value=f"${data['market_data']['market_cap']['usd'] / 1e9:.1f}B", inline=False)
            embed.add_field(name="24-Hour Volume", value=f"${data['market_data']['total_volume']['usd'] / 1e9:.1f}B", inline=False)
            embed.add_field(name="High/Low (24h)", value=f"${data['market_data']['high_24h']['usd']:,.2f} / ${data['market_data']['low_24h']['usd']:,.2f}", inline=False)
            embed.add_field(name="Circulating Supply", value=f"{data['market_data']['circulating_supply'] / 1e6:.1f}M {data['symbol'].upper()}", inline=False)
            embed.add_field(name="All-Time High", value=f"${data['market_data']['ath']['usd']:,.2f}", inline=False)
            embed.set_footer(text="Data powered by CoinGecko")

            await ctx.response.send_message(embed=embed)

# Example usage
if __name__ == "__main__":
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    bot = app_commands.CommandTree(client)
    guild_id = 1320393932378603644
    crypto_info_command = CryptoInfoCommand(bot, client, guild_id)
    asyncio.run(crypto_info_command.register())