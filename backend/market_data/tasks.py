from celery import shared_task
from django.core.cache import cache
from market_data.services.market_provider import TemporaryProviderError
from market_data.services.market_data_service import MarketDataService
import requests
import redis

@shared_task(
    autoretry_for=(requests.exceptions.Timeout, TemporaryProviderError),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def sync_asset_prices(symbol):
    redis_client = redis.Redis(
        host="localhost",
        port=6380,
        db=0,
    )
    lock_key = f"market_data:sync:{symbol}"
    lock = redis_client.lock(lock_key, timeout=300)

    acquired = lock.acquire(blocking=False)
    if not acquired:
        # If the lock is already acquired, it means another task is running for this symbol
        return

    try:
        service = MarketDataService()
        service.fetch_and_store_daily_prices(symbol)
        cache.delete(f"market_data:prices:{symbol}:latest")
        cache.delete(f"market_data:prices:all")
    finally:
        lock.release()
    
