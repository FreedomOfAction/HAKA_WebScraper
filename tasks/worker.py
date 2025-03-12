from celery import Celery
from scraper.broker_api import BrokerAPI
from scraper.broker_scraper import BrokerScraper
import re

# Initialize Celery with Redis
celery = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@celery.task
def scrape_broker(url_or_name):
    """Automatically detects API availability or scrapes the broker website."""
    try:
        # ✅ If input is a URL, use web scraping
        if re.match(r"https?://", url_or_name):
            scraper = BrokerScraper(url_or_name)
            data = scraper.scrape_assets()
        else:
            # ✅ Otherwise, check if API is available and use it
            api_client = BrokerAPI(url_or_name)
            data = api_client.get_trading_assets()

        # ✅ Ensure response is always a dictionary
        if not isinstance(data, dict):
            return {"error": "Invalid data format"}

        return data

    except Exception as e:
        return {"error": str(e)}
