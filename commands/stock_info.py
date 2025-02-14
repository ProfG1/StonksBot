import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
import yfinance as yf
import random
import os
from dotenv import load_dotenv

class StockInfoCommand:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self):
        @self.bot.command(name="stock_info", description="Get stock information", guild=discord.Object(id=self.guild_id))
        async def stock_info(ctx: discord.Interaction, ticker: str):
            load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
            logo_api_key = os.getenv("LOGO")

            stock = yf.Ticker(ticker)
            info = stock.info

            # Basic Information
            stock_ticker = ticker
            company_name = info.get("shortName", "N/A")
            exchange = info.get("exchange", "N/A")
            current_price = info.get("currentPrice", "N/A")
            previous_close = info.get("previousClose", "N/A")
            price_change = current_price - previous_close if current_price != "N/A" and previous_close != "N/A" else "N/A"
            price_change_percent = (price_change / previous_close * 100) if price_change != "N/A" and previous_close != "N/A" else "N/A"

            # Additional Metrics
            high_low_day = f"{info.get('dayHigh', 'N/A')} / {info.get('dayLow', 'N/A')}"
            opening_price = info.get("open", "N/A")
            market_cap = info.get("marketCap", "N/A")
            volume = info.get("volume", "N/A")
            range_52_week = f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}"

            # Create an embed with randomized color
            embed = discord.Embed(title="Stock Information", color=random.randint(0, 0xFFFFFF))
            embed.add_field(name="Stock Ticker", value=stock_ticker, inline=False)
            embed.add_field(name="Company Name", value=company_name, inline=False)
            embed.add_field(name="Exchange", value=exchange, inline=False)
            embed.add_field(name="Current Price", value=f"${current_price}", inline=False)
            embed.add_field(name="Price Change", value=f"{price_change:+.2f} ({price_change_percent:+.2f}%)", inline=False)
            embed.add_field(name="High/Low of the Day", value=high_low_day, inline=False)
            embed.add_field(name="Opening Price", value=f"${opening_price}", inline=False)
            embed.add_field(name="Market Cap", value=f"${market_cap}", inline=False)
            embed.add_field(name="Volume", value=volume, inline=False)
            embed.add_field(name="52-Week Range", value=range_52_week, inline=False)

            # Add company logo to the embed
            domain = info.get("website", "N/A").replace("https://", "").replace("http://", "").split('/')[0]
            logo_url = f"https://img.logo.dev/{domain}?token={logo_api_key}"
            embed.set_thumbnail(url=logo_url)

            # Add footer to the embed
            embed.set_footer(text="Data powered by Yahoo Finance and Clearbit Logo")

            await ctx.response.send_message(embed=embed)


if __name__ == "__main__":
    ticker = "TSLA"
    print(StockInfoCommand(ticker))