from celery import shared_task
from market_data.services.market_provider import TemporaryProviderError
from market_data.services.market_data_service import MarketDataService
import requests

@shared_task(
    autoretry_for=(requests.exceptions.Timeout, TemporaryProviderError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def sync_asset_prices(symbol):
    service = MarketDataService()
    service.fetch_and_store_daily_prices(symbol)
    
