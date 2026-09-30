from assets.models import Asset
from market_data.models import Price
from market_data.services.market_provider import AlphaVantageProvider

class MarketDataService:
    def __init__(self):
        self.provider = AlphaVantageProvider()
    
    def fetch_and_store_daily_prices(self, symbol):
        asset = Asset.objects.get(symbol=symbol)
        daily_prices = self.provider.get_daily_prices(symbol)

        print("Asset:", asset)
        print("Prices received:", len(daily_prices))

        for price_data in daily_prices:
            print("Saving:", price_data["date"])

            obj, created = Price.objects.update_or_create(
                asset=asset,
                date=price_data["date"],
                defaults={
                    "open_price": price_data["open_price"],
                    "high_price": price_data["high_price"],
                    "low_price": price_data["low_price"],
                    "close_price": price_data["close_price"],
                },
            )

            print("Created:", created, "->", obj)