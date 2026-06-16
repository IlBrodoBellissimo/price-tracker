import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class PriceTracker:
    def __init__(self, url, target_price):
        self.url = url
        self.target_price = float(target_price)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
    def get_price(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            price_selectors = ['.a-price-whole', '.a-offscreen', '.current-price']
            
            for selector in price_selectors:
                element = soup.select_one(selector)
                if element:
                    price_text = element.get_text().strip()
                    price_clean = ''.join([c for c in price_text if c.isdigit() or c == '.'])
                    if price_clean:
                        return float(price_clean)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def check_price(self):
        current_price = self.get_price()
        if current_price is None:
            print(f"[{datetime.now()}] Could not retrieve price")
            return False
            
        print(f"[{datetime.now()}] Current: ${current_price:.2f} | Target: ${self.target_price:.2f}")
        
        if current_price <= self.target_price:
            print("TARGET REACHED!")
            return True
        return False

if __name__ == "__main__":
    tracker = PriceTracker("https://example.com/product", 100.00)
    tracker.check_price()
