import os

import requests
from dotenv import load_dotenv
def search_symbol(api_key, keywords):
    """
    Search for a stock symbol using the Alpha Vantage API.

    Parameters:
    api_key (str): Your Alpha Vantage API key.
    keywords (str): The keywords to search for.
# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
    Returns:
    dict: The JSON response from the API containing search results.
    """
def search_symbol(api_key, keywords):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keywords}&apikey={api_key}'
    response = requests.get(url)
    return response.json()

# Example usage
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env')) # Load environment variables from .env file
api_key: str = os.getenv("ALPHA_VANTAGE_API_KEY")
keywords = 'Tesla Inc'
search_symbol(api_key, keywords)