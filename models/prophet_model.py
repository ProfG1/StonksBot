from prophet import Prophet
import pandas as pd

def predict_stock_prices(data, period):
    """
    Predict stock prices using Facebook Prophet.

    Parameters:
    data (pd.DataFrame): Historical stock price data with columns 'ds' (date) and 'y' (price).
    period (str): Prediction period ('1d', '7d', '30d', '90d', '1y').

    Returns:
    pd.DataFrame: DataFrame containing the forecasted prices.
    """
    model = Prophet()
    model.fit(data)

    if period == '1d':
        future = model.make_future_dataframe(periods=1)
    elif period == '7d':
        future = model.make_future_dataframe(periods=7)
    elif period == '30d':
        future = model.make_future_dataframe(periods=30)
    elif period == '90d':
        future = model.make_future_dataframe(periods=90)
    elif period == '1y':
        future = model.make_future_dataframe(periods=365)
    else:
        raise ValueError("Invalid period. Choose from '1d', '7d', '30d', '90d', '1y'.")

    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
