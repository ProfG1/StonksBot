# StonksBot

StonksBot is a Discord bot designed to provide stock and cryptocurrency information, along with various financial metrics and predictions. The bot leverages multiple APIs to fetch the latest data and presents it in an easy-to-read format within Discord.

## Key Features
- **Prediction**: Predict using regression models the future price of the data given a timeframe using `/predict ` command .
- **Real-Time Stock Information**: Get the latest stock prices, market cap, volume, and other key metrics using the `/stock_info` command.
- **Cryptocurrency Information**: Fetch current prices, market cap, volume, and other details for various cryptocurrencies using the `/crypto_info` command.
- **Stock Symbol Search**: Search for stock symbols using keywords with the `/symbol_search` command.
- **Ping Command**: Check the bot's latency with the `/ping` command.
- **Interactive UI**: Use Discord's slash commands for a seamless user experience.

## Under Development

- **Redis Caching**: Implement caching to improve response times and reduce API calls.
- **News**: Provides financial news with optional arguments such as the topic, ticker, and time.
- **News Sentiment Analysis**: Uses OpenAI API to analyze if the news is bullish or bearish.
- **Trading Signals**: Add "Buy" / "Sell" signals based on prediction trends. Example: If predicted price rises, recommend a BUY.
- **User Interaction & Polls**: Allow users to vote on AI predictions. Collect user feedback and improve accuracy.
- **Prediction**: Enhance prediction algorithms for better accuracy.

## Stock & Crypto Price Prediction Timeframes

| ⏳ Time Argument  | Description                         | Best Use Case           |
|-------------------|-------------------------------------|-------------------------|
| **1d (1 day)**    | Predicts tomorrow’s price           | Short-term trading      |
| **7d (1 week)**   | Predicts next week's trend          | Swing trading           |
| **30d (1 month)** | Estimates the next month's price    | Medium-term investments |
| **90d (3 months)**| Long-term trend forecasting         | Investors               |
| **1y (1 year)**   | Predicts annual trends              | Market outlook          |


## Libraries and APIs Used

- **Discord.py**: A Python wrapper for the Discord API.
- **Yahoo Finance API**: Provides real-time and historical stock market data.
- **Alpha Vantage API**: Provides company and ticker information.
- **CoinGecko API**: Fetches cryptocurrency data including prices, market cap, and volume.
- **Prophet**: A forecasting tool used for predicting time series data.