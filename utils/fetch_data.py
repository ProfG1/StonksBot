import os
import requests
from dotenv import load_dotenv
import logging
import yfinance as yf
import joblib
import time
from pathlib import Path

logger = logging.getLogger(__name__)

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
DATA_CACHE_DIR = CACHE_DIR / "data"
DATA_CACHE_DIR.mkdir(exist_ok=True)

# TTL values in seconds
TTL_CRYPTO = 30 * 60  # 30 minutes
TTL_STOCK_DAILY = 6 * 60 * 60  # 6 hours
TTL_STOCK_WEEKLY = 24 * 60 * 60  # 24 hours
TTL_STOCK_LONG_TERM = 7 * 24 * 60 * 60  # 7 days

def search_symbol(api_key, keywords):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={api_key}'
    response = requests.get(url)
    return response.json()

def get_crypto_info(crypto_id, api_key):
    cache_key = f"crypto_{crypto_id}"
    cache_file = DATA_CACHE_DIR / f"{cache_key}.pkl"
    
    if cache_file.exists():
        data = joblib.load(cache_file)
        cache_time = os.path.getmtime(cache_file)
        if time.time() - cache_time < TTL_CRYPTO:
            logger.info(f"Retrieved cached data for {crypto_id}")
            return data

    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}?x_cg_demo_api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        joblib.dump(data, cache_file)
        logger.info(f"Successfully fetched data for {crypto_id}")
        return data
    return None

def fetch_stock_data(ticker, period, interval):
    cache_key = f"{ticker}_{period}_{interval}"
    cache_file = DATA_CACHE_DIR / f"{cache_key}.pkl"
    
    ttl = TTL_STOCK_DAILY
    if period in ['60d', '180d']:
        ttl = TTL_STOCK_WEEKLY
    elif period in ['2y']:
        ttl = TTL_STOCK_LONG_TERM

    if cache_file.exists():
        data = joblib.load(cache_file)
        cache_time = os.path.getmtime(cache_file)
        if time.time() - cache_time < ttl:
            logger.info(f"Retrieved cached data for {ticker}")
            return data

    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    
    if data.empty:
        logger.error(f"No data retrieved for ticker {ticker}")
        return None
        
    joblib.dump(data, cache_file)
    logger.info(f"Successfully fetched {len(data)} records for {ticker}")
    return data

if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    keywords = 'Tesla Inc'
    print(search_symbol(api_key, keywords))

    crypto_api_key = os.getenv("CRYPTO")
    crypto_id = 'bitcoin'
    print(get_crypto_info(crypto_id, crypto_api_key))
