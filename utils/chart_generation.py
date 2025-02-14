import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging

class StockChartGenerator:
    def __init__(self, output_dir="cache/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Color scheme
        self.colors = {
            'up_candle': '#26A69A',       # Green for up moves
            'down_candle': '#EF5350',      # Red for down moves
            'prediction': '#5C6BC0',       # Indigo for prediction line
            'volume_up': 'rgba(38, 166, 154, 0.3)',
            'volume_down': 'rgba(239, 83, 80, 0.3)',
            'bounds': (92/255, 107/255, 192/255, 0.2)  # Light indigo for bounds
        }
        
        # Static image config
        self.image_config = {
            'width': 1200,
            'height': 800,
            'scale': 2  # High res
        }

    def generate_candlestick_chart(self, data, forecast, ticker, period):
        try:
            fig, ax = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
            
            ax[0].plot(data['Date'], data['Close'], label='Close Price', color='black')
            ax[0].fill_between(forecast['Date'], forecast['Lower_Bound'], forecast['Upper_Bound'], color=self.colors['bounds'], alpha=0.3, label='Confidence Interval')
            ax[0].plot(forecast['Date'], forecast['Predicted_Price'], label='Predicted Price', color=self.colors['prediction'], linestyle='--')
            ax[0].set_title(f"{ticker} Price Action & Predictions ({period})")
            ax[0].set_ylabel('Price')
            ax[0].legend()

            ax[1].bar(data['Date'], data['Volume'], color='blue', alpha=0.6)
            ax[1].set_ylabel('Volume')
            ax[1].set_xlabel('Date')

            plt.tight_layout()
            output_path = self.output_dir / f"{ticker}_candlestick_{period}.png"
            plt.savefig(output_path)
            plt.close(fig)
            
            self.logger.info(f"Candlestick chart saved to {output_path}")
            return str(output_path)

        except Exception as e:
            self.logger.error(f"Error generating candlestick chart: {str(e)}")
            return None

    def generate_line_chart(self, data, forecast, ticker, period):
        try:
            fig, ax = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

            ax[0].plot(data['Date'], data['Close'], label='Close Price', color='black')
            ax[0].fill_between(forecast['Date'], forecast['Lower_Bound'], forecast['Upper_Bound'], color=self.colors['bounds'], alpha=0.3, label='Confidence Interval')
            ax[0].plot(forecast['Date'], forecast['Predicted_Price'], label='Predicted Price', color=self.colors['prediction'], linestyle='--')
            ax[0].set_title(f"{ticker} Price Trend & Predictions ({period})")
            ax[0].set_ylabel('Price')
            ax[0].legend()

            ax[1].bar(data['Date'], data['Volume'], color='blue', alpha=0.6)
            ax[1].set_ylabel('Volume')
            ax[1].set_xlabel('Date')

            plt.tight_layout()
            output_path = self.output_dir / f"{ticker}_line_{period}.png"
            plt.savefig(output_path)
            plt.close(fig)
            
            self.logger.info(f"Line chart saved to {output_path}")
            return str(output_path)

        except Exception as e:
            self.logger.error(f"Error generating line chart: {str(e)}")
            return None

def generate_charts(data, forecast, ticker, period):
    chart_gen = StockChartGenerator()
    
    # Generate both charts
    candlestick_path = chart_gen.generate_candlestick_chart(data, forecast, ticker, period)
    line_path = chart_gen.generate_line_chart(data, forecast, ticker, period)
    
    return candlestick_path, line_path