from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import logging
from .config import config

logging.basicConfig(level=logging.INFO)

class TradingScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
        self.driver = webdriver.Chrome(service=Service(config.SELENIUM_DRIVER_PATH), options=chrome_options)

    def scrape_static(self, url):
        """Extracts broker data from static HTML pages."""
        headers = {"User-Agent": config.USER_AGENT}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "broker_name": soup.find("h1", class_="broker-title").text.strip(),
            "supported_assets": [a.text for a in soup.select("ul.assets-list li")],
            "trading_fees": soup.find("span", class_="trading-fees").text.strip()
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
