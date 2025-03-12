from celery import Celery
from scraper.scraper import TradingScraper
from scraper.parser import clean_data, to_json
import logging
from scraper.config import config

app = Celery('tasks', broker=config.REDIS_URL)

@app.task
def scrape_broker(url):
    """Runs the scraper as an asynchronous Celery task."""
    scraper = TradingScraper()
    raw_data = scraper.scrape_static(url)
    structured_data = clean_data(raw_data)
    scraper.close()
    return to_json(structured_data)
