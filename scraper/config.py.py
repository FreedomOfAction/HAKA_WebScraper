import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = "https://example-trading-broker.com"
    SELENIUM_DRIVER_PATH = os.getenv("SELENIUM_DRIVER_PATH", "./chromedriver")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

config = Config()
