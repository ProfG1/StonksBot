from prophet import Prophet
import pandas as pd
import logging
import joblib
from pathlib import Path

logger = logging.getLogger(__name__)

MODEL_CACHE_DIR = Path("cache/models")
MODEL_CACHE_DIR.mkdir(exist_ok=True)

def prepare_data_for_prophet(stock_data):
    """
    Prepare stock data for Prophet.
    """
    df = stock_data.reset_index()[['Date', 'Close']]
    df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)
    df['y'] = df['y'].astype(float)
    df = df.dropna()
    df = df.drop_duplicates(subset=['ds'])
    return df

def get_cached_model(ticker, period):
    """
    Get cached Prophet model.
    """
    cache_key = f"{ticker}_{period}"
    model_file = MODEL_CACHE_DIR / f"{cache_key}.pkl"
    
    if model_file.exists():
        try:
            return joblib.load(model_file)
        except:
            return None
    return None

def save_model_to_cache(model, ticker, period):
    """
    Save Prophet model to cache.
    """
    cache_key = f"{ticker}_{period}"
    model_file = MODEL_CACHE_DIR / f"{cache_key}.pkl"
    joblib.dump(model, model_file)

def predict_stock_prices(data, period, ticker):
    try:
        model = get_cached_model(ticker, period)
        
        if model is None:
            model = Prophet(
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05,
                interval_width=0.95
            )
            model.fit(data)
            save_model_to_cache(model, ticker, period)
        
        period_mapping = {
            '1d': 1, '7d': 7, '30d': 30,
            '90d': 90, '1y': 365
        }
        
        periods = period_mapping.get(period)
        if not periods:
            raise ValueError(f"Invalid period: {period}")
        
        future = model.make_future_dataframe(
            periods=periods,
            freq='D' if period != '1d' else 'H'
        )
        
        forecast = model.predict(future)
        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        result.columns = ['Date', 'Predicted_Price', 'Lower_Bound', 'Upper_Bound']
        
        return result

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return None