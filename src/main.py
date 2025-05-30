import discord
from discord.ext import commands
import os
import asyncio
import logging
from dotenv import load_dotenv
from events.on_ready import OnReadyEvent
from commands.ping import PingCommand
from commands.ticker_search import TickerSearchCommand
from commands.stock_info import StockInfoCommand
from commands.crypto_info import CryptoInfoCommand
from commands.predict import PredictCommand
from config.logging_config import setup_logging
from const_online import const_online

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

const_online

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
TOKEN: str = os.getenv("TOKEN")
COMMANDS_PATH: str = os.getenv("COMMANDS_PATH", "src/commands")
if TOKEN is None:
    logger.error("No TOKEN found in environment variables")
    raise ValueError("No TOKEN found in environment variables")

# Initialize bot with appropriate intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize event and command handlers
guild_id = 1320393932378603644
on_ready_event = OnReadyEvent(bot.tree, bot, guild_id)
ping_command = PingCommand(bot.tree, bot, guild_id)
ticker_search_command = TickerSearchCommand(bot.tree, bot, guild_id)
stock_info_command = StockInfoCommand(bot.tree, bot, guild_id)
crypto_info_command = CryptoInfoCommand(bot.tree, bot, guild_id)
predict_command = PredictCommand(bot.tree, bot, guild_id)

@bot.event
async def on_ready():
    await on_ready_event.on_ready()
    logger.info(f'Bot logged in as {bot.user} ({bot.user.id})')

@bot.event
async def on_command(ctx):
    logger.info(f'Command used: {ctx.command} by {ctx.author} in {ctx.channel}')

@bot.event
async def on_command_error(ctx, error):
    logger.error(f'Error in command {ctx.command}: {error}')

async def load_commands(): # Load all commands from the commands dir 
    await ping_command.register()
    await ticker_search_command.register()
    await stock_info_command.register()
    await crypto_info_command.register()
    await predict_command.register()
    for filename in os.listdir(COMMANDS_PATH):
        if filename.endswith('.py') and filename not in ['ping.py', 'ticker_search.py', 'stock_info.py', 'crypto_info.py', 'predict.py']:
            await bot.load_extension(f'commands.{filename[:-3]}')
    logger.info("All commands loaded")

async def main(): # starts the bot
    await load_commands()
    await bot.start(TOKEN)
    
asyncio.run(main())