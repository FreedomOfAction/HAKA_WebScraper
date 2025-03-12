import unittest
from scraper.scraper import TradingScraper

class TestTradingScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = TradingScraper()

    def test_scrape_static(self):
        url = "https://example-trading-broker.com"
        data = self.scraper.scrape_static(url)
        self.assertIn("broker_name", data)
        self.assertIn("supported_assets", data)

    def tearDown(self):
        self.scraper.close()

if __name__ == "__main__":
    unittest.main()
