import discord
from discord import app_commands
from discord.ext import commands
import os
import pandas as pd
import asyncio
from dotenv import load_dotenv
from utils.fetch_data import fetch_stock_data
from models.prophet_model import prepare_data_for_prophet, predict_stock_prices
from utils.chart_generation import StockChartGenerator
import logging
import time

logger = logging.getLogger(__name__)

class PredictCommand:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self):
        @self.bot.command(name="predict", description="Predict stock prices", guild=discord.Object(id=self.guild_id))
        @app_commands.describe(ticker="The stock ticker symbol", period="Prediction period", chart_type="Type of chart (candlestick or line)")
        @app_commands.choices(period=[
            app_commands.Choice(name="1 day", value="1d"),
            app_commands.Choice(name="7 days", value="7d"),
            app_commands.Choice(name="30 days", value="30d"),
            app_commands.Choice(name="90 days", value="90d"),
            app_commands.Choice(name="1 year", value="1y")
        ])
        @app_commands.choices(chart_type=[
            app_commands.Choice(name="Candlestick", value="candlestick"),
            app_commands.Choice(name="Line", value="line")
        ])
        async def predict(ctx: discord.Interaction, ticker: str, period: app_commands.Choice[str], chart_type: app_commands.Choice[str] = "candlestick"):
            await ctx.response.defer() 

            load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                await ctx.followup.send("API key not found.", ephemeral=True)
                return

            period_mappings = {
                '1d': {'period': '2d', 'interval': '1m'},
                '7d': {'period': '14d', 'interval': '15m'},
                '30d': {'period': '60d', 'interval': '1d'},
                '90d': {'period': '180d', 'interval': '1d'},
                '1y': {'period': '2y', 'interval': '1wk'}
            }

            if period.value not in period_mappings:
                await ctx.followup.send("Invalid period.", ephemeral=True)
                return

            stock_data = fetch_stock_data(ticker, period_mappings[period.value]['period'], period_mappings[period.value]['interval'])
            if stock_data is None:
                await ctx.followup.send("Failed to retrieve stock data. Please check the ticker symbol and try again.", ephemeral=True)
                return

            stock_data.reset_index(inplace=True)
            stock_data.rename(columns={'index': 'Date'}, inplace=True)

            prepared_data = prepare_data_for_prophet(stock_data)
            if prepared_data is None:
                await ctx.followup.send("Failed to prepare data for prediction.", ephemeral=True)
                return

            forecast = predict_stock_prices(prepared_data, period.value, ticker)
            if forecast is None:
                await ctx.followup.send("Failed to generate predictions.", ephemeral=True)
                return

            forecast.rename(columns={'ds': 'Date'}, inplace=True)

            # Generate and cache the chart
            chart_gen = StockChartGenerator(output_dir="cache/charts")
            if chart_type.value == "candlestick":
                chart_path = chart_gen.generate_candlestick_chart(stock_data, forecast, ticker, period.value)
            else:
                chart_path = chart_gen.generate_line_chart(stock_data, forecast, ticker, period.value)

            if chart_path:
                await ctx.followup.send(file=discord.File(chart_path))
            else:
                await ctx.followup.send("Failed to generate chart.", ephemeral=True)

if __name__ == "__main__":
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    bot = app_commands.CommandTree(client)
    guild_id = 1320393932378603644
    predict_command = PredictCommand(bot, client, guild_id)
    asyncio.run(predict_command.register())