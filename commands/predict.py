import discord
from discord import app_commands
from discord.ext import commands
import os
import pandas as pd
import asyncio
from dotenv import load_dotenv
from utils.fetch_data import search_symbol
from models.prophet_model import predict_stock_prices
from utils.chart_generation import generate_candlestick_chart

class PredictCommand:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self):
        @self.bot.command(name="predict", description="Predict stock prices", guild=discord.Object(id=self.guild_id))
        @app_commands.describe(ticker="The stock ticker symbol", period="Prediction period")
        @app_commands.choices(period=[
            app_commands.Choice(name="1 day", value="1d"),
            app_commands.Choice(name="7 days", value="7d"),
            app_commands.Choice(name="30 days", value="30d"),
            app_commands.Choice(name="90 days", value="90d"),
            app_commands.Choice(name="1 year", value="1y")
        ])
        async def predict(ctx: discord.Interaction, ticker: str, period: app_commands.Choice[str]):
            load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                await ctx.response.send_message("API key not found.", ephemeral=True)
                return

            # Fetch historical stock price data
            data = search_symbol(api_key, ticker)
            if not data or 'bestMatches' not in data:
                await ctx.response.send_message("Failed to retrieve stock data.", ephemeral=True)
                return

            # Prepare data for Prophet
            historical_data = pd.DataFrame(data['bestMatches'])
            historical_data.rename(columns={'1. symbol': 'ds', '2. name': 'y'}, inplace=True)
            historical_data['ds'] = pd.to_datetime(historical_data['ds'])
            historical_data['y'] = historical_data['y'].astype(float)

            # Predict stock prices
            forecast = predict_stock_prices(historical_data, period.value)

            # Generate candlestick chart
            filename = f"{ticker}_{period.value}.png"
            generate_candlestick_chart(historical_data, forecast, filename)

            # Send the chart to Discord
            await ctx.response.send_message(file=discord.File(filename))

# Example usage
if __name__ == "__main__":
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    bot = app_commands.CommandTree(client)
    guild_id = 1320393932378603644
    predict_command = PredictCommand(bot, client, guild_id)
    asyncio.run(predict_command.register())
