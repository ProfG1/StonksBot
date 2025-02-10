import os
import requests
from dotenv import load_dotenv

def search_symbol(api_key, keywords):
    """
    Search for a stock symbol using the Alpha Vantage API.

    Parameters:
    api_key (str): Your Alpha Vantage API key.
    keywords (str): The keywords to search for.

    Returns:
    dict: The JSON response from the API containing search results.
    """
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={api_key}'
    response = requests.get(url)
    return response.json()

def get_crypto_info(crypto_id, api_key):
    """
    Get detailed information about a cryptocurrency using the CoinGecko API.

    Parameters:
    crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
    api_key (str): Your CoinGecko API key.

    Returns:
    dict: The JSON response from the API containing cryptocurrency information.
    """
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}?x_cg_demo_api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Example usage
if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    keywords = 'Tesla Inc'
    print(search_symbol(api_key, keywords))

    crypto_api_key = os.getenv("CRYPTO")
    crypto_id = 'bitcoin'
    print(get_crypto_info(crypto_id, crypto_api_key))
