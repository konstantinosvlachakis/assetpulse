import os

import requests
from dotenv import load_dotenv


load_dotenv()

class TemporaryProviderError(Exception):
    """Custom exception for temporary provider errors."""
    pass


class AlphaVantageProvider:

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    def get_daily_prices(self, symbol):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=10,
        )
        
        if response.status_code == 503:
            raise TemporaryProviderError("Alpha Vantage service is temporarily unavailable.")
        
        response.raise_for_status()

  
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        
        prices = []
        for date, price_data in time_series.items():
            prices.append({
                "date": date,
                "open_price": price_data["1. open"],
                "high_price": price_data["2. high"],
                "low_price": price_data["3. low"],
                "close_price": price_data["4. close"],
            })
        
        return prices
