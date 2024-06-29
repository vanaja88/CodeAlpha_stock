import requests
import json
from datetime import datetime

# Replace 'YOUR_API_KEY' with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = 'YOUR_API_KEY'

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {'shares': shares, 'purchase_prices': []}

    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            if shares >= self.portfolio[symbol]['shares']:
                del self.portfolio[symbol]
            else:
                self.portfolio[symbol]['shares'] -= shares

    def get_portfolio_value(self):
        total_value = 0.0
        for symbol, data in self.portfolio.items():
            latest_price = self.get_latest_price(symbol)
            if latest_price is not None:
                stock_value = latest_price * data['shares']
                total_value += stock_value
        return total_value

    def get_latest_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            latest_price = float(data['Global Quote']['05. price'])
            return latest_price
        except (requests.RequestException, KeyError) as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def print_portfolio(self):
        print("\nCurrent Portfolio:")
        for symbol, data in self.portfolio.items():
            latest_price = self.get_latest_price(symbol)
            if latest_price is not None:
                current_value = latest_price * data['shares']
                print(f"{symbol}: {data['shares']} shares, Current Price: ${latest_price:.2f}, Current Value: ${current_value:.2f}")
            else:
                print(f"{symbol}: {data['shares']} shares (Price data unavailable)")

# Example usage
def main():
    portfolio = StockPortfolio()

    # Add some stocks to the portfolio
    portfolio.add_stock("AAPL", 5)
    portfolio.add_stock("GOOGL", 2)

    # Print initial portfolio
    portfolio.print_portfolio()

    # Simulate a market update
    print("\nUpdating portfolio values...")
    print(f"Total Portfolio Value: ${portfolio.get_portfolio_value():.2f}")

    # Remove some stocks
    portfolio.remove_stock("AAPL", 2)

    # Print updated portfolio
    portfolio.print_portfolio()

if __name__ == "__main__":
    main()
