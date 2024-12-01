import yfinance as yf
import pandas as pd
import requests
from typing import Dict, Optional

class StockDataFetcher:
    def __init__(self, k):
        # Configure pandas display options
        pd.set_option('display.width', None)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.float_format', '{:,.2f}'.format)
        self.instruments_to_fetch_count = k

    def get_historical_market_cap(self, ticker_symbol: str, period: str) -> pd.DataFrame:
        """Fetches historical market cap data for a given ticker."""
        ticker = yf.Ticker(ticker_symbol)
        historical_data = ticker.history(period=period)
        historical_data = historical_data[::-1]
        historical_data.index = historical_data.index.date

        historical_data = historical_data.reset_index()

        historical_data.rename(columns={'index': 'Date', 'Close': 'Share Price'}, inplace=True)

        shares_outstanding = ticker.info.get("sharesOutstanding")
        
        if not shares_outstanding:
            raise ValueError(f"Shares outstanding data not available for {ticker_symbol}")

        historical_data['Cumulative Split Factor'] = historical_data['Stock Splits'].copy()
        historical_data.loc[ historical_data['Cumulative Split Factor'] == 0, 'Cumulative Split Factor'] = 1
        historical_data['Cumulative Split Factor'] = historical_data['Cumulative Split Factor'].cumprod()

        historical_data['Effective Shares Outstanding'] = shares_outstanding / historical_data['Cumulative Split Factor']
        historical_data['Market Cap'] = historical_data['Share Price'] * historical_data['Effective Shares Outstanding']

        # print(f"historical_data: {type(historical_data.iloc[0]['Date'])}")
        return historical_data[['Date', 'Share Price', 'Market Cap', 'Effective Shares Outstanding']]

    def get_us_stocks_universe(self, period: str = "1y") -> Dict[str, pd.DataFrame]:
        """Fetches data for US stocks from Nasdaq API."""
        nasdaq_url = f'https://api.nasdaq.com/api/screener/stocks?limit={self.instruments_to_fetch_count}'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

        try:
            response = requests.get(nasdaq_url, headers=headers)
            nasdaq_data = response.json()
            nasdaq_tickers = [
                row['symbol'].replace('/', '-') 
                for row in nasdaq_data['data']['table']['rows']
            ]
        except Exception as e:
            raise ConnectionError(f"Error fetching stock universe: {e}")

        universe_data = {}
        for ticker in nasdaq_tickers:
            try:
                data = self.get_historical_market_cap(ticker, period)
                universe_data[ticker] = data
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")

        return universe_data
