from celery import shared_task
from market_data.services.market_data_service import MarketDataService

@shared_task
def sync_asset_prices(symbol):
    service = MarketDataService()
    service.fetch_and_store_daily_prices(symbol)