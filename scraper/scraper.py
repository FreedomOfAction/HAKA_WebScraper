from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import logging
from .config import REDIS_URL, USER_AGENT  # ✅ Import only variables

logging.basicConfig(level=logging.INFO)

class TradingScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
        self.driver = webdriver.Chrome(service=Service(config.SELENIUM_DRIVER_PATH), options=chrome_options)

    def scrape_static(self, url):
        """Extracts broker data from static HTML pages."""
        headers = {"User-Agent": config.USER_AGENT}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "broker_name": soup.find("h1").text.strip() if soup.find("h1") else "Not Found",
            "trading_assets": [a.text.strip() for a in soup.select("ul.assets-list li")] if soup.select("ul.assets-list li") else ["No Assets Found"]
        }
        return data

    def scrape_dynamic(self, url):
        """Handles JavaScript-loaded broker pages using Selenium."""
        self.driver.get(url)
        assets = self.driver.find_elements("css selector", ".asset-item")
        asset_list = [asset.text for asset in assets]
        return {"trading_assets": asset_list}

    def close(self):
        self.driver.quit()
