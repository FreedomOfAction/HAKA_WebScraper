import requests
from bs4 import BeautifulSoup

class BrokerScraper:
    def __init__(self, broker_url):
        """Initialize the scraper with the broker's URL."""
        self.broker_url = broker_url

    def scrape_assets(self):
        """Tries to extract asset lists from the broker's website dynamically."""
        try:
            response = requests.get(self.broker_url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                return self._parse_html(response.text)
            else:
                return {"error": f"Failed to fetch page, status code: {response.status_code}"}
        except Exception as e:
            return {"error": f"Web scraping failed: {str(e)}"}

    def _parse_html(self, html):
        """Extracts trading assets from the page dynamically."""
        soup = BeautifulSoup(html, "html.parser")

        # Look for asset lists inside <div> elements
        asset_sections = soup.find_all("div", class_="asset-list")  
        assets = []

        for section in asset_sections:
            asset_names = section.find_all("span", class_="asset-name")
            assets.extend([a.text.strip() for a in asset_names])

        # If no assets are found, return an appropriate message
        return {"trading_assets": assets if assets else ["No assets found"]}
