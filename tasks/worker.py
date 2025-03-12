from celery import Celery
from scraper.scraper import TradingScraper
from scraper.config import REDIS_URL  # ✅ Correct import

# ✅ Correct Celery initialization
celery = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

celery.conf.update(
    result_backend=REDIS_URL,
    task_serializer="json",
    accept_content=["json"],
    result_expires=3600,
)

@celery.task
def scrape_broker(url):
    """Runs the scraper as an asynchronous Celery task."""
    scraper = TradingScraper()
    data = scraper.scrape_static(url)
    scraper.close()
    return data
