import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

def generate_candlestick_chart(data, forecast, filename):
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    forecast['ds'] = pd.to_datetime(forecast['ds'])
    forecast.set_index('ds', inplace=True)

    # Combine historical and forecasted data
    combined = pd.concat([data, forecast[['yhat']]], axis=1)

    # Plot the candlestick chart
    mpf.plot(combined, type='candle', style='charles', volume=True, savefig=filename)



