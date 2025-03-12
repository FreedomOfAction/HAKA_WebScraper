import requests

class BrokerAPI:
    def __init__(self, broker_name, api_key=None):
        self.broker_name = broker_name.lower()
        self.api_key = api_key
        self.base_urls = {
            "binance": "https://api.binance.com/api/v3/",
            "kucoin": "https://api.kucoin.com/api/v1/",
            "cexio": "https://cex.io/api/"
        }

    def get_trading_assets(self):
        """Detects the correct API endpoint and extracts asset lists."""
        if self.broker_name in self.base_urls:
            return self._fetch_assets(self.base_urls[self.broker_name])
        return {"error": "Unsupported broker API"}

    def _fetch_assets(self, api_url):
        """Fetches trading assets from the broker API."""
        try:
            response = requests.get(api_url + "exchangeInfo")
            if response.status_code == 200:
                data = response.json()
                if "symbols" in data:
                    trading_assets = [symbol["symbol"] for symbol in data["symbols"]]
                    return {"trading_assets": trading_assets}
                return {"error": "Invalid response format"}
            return {"error": f"API request failed with status {response.status_code}"}
        except Exception as e:
            return {"error": f"API request error: {str(e)}"}
