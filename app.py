import streamlit as st
import pandas as pd
from datetime import datetime
from src.data.stock_data_fetcher import StockDataFetcher
from src.data.database_manager import DatabaseManager
from src.index.hedgineer_index import HedgineerIndex
from src.visualization.dashboard import Dashboard
from constants import LOOKBACK_DAYS_FOR_UI, INDEX_CONSTITUENTS_COUNT, DATA_STORE_PERIOD, INSTRUMENTS_TO_FETCH
def main():
    # Initialize components
    db_manager = DatabaseManager()
    stock_fetcher = StockDataFetcher(INSTRUMENTS_TO_FETCH)
    
    # Fetch and store data
    us_stocks = stock_fetcher.get_us_stocks_universe(DATA_STORE_PERIOD)
    db_manager.insert_stock_data(us_stocks)
    
    # Initialize index
    Hedgineer_index = HedgineerIndex(db_manager.cursor)
    
    # Calculate index for last LOOKBACK_DAYS_FOR_UI days
    for date in pd.date_range(datetime.now(), periods=LOOKBACK_DAYS_FOR_UI, freq='-1D').strftime('%Y-%m-%d'):
        Hedgineer_index.calculate_index_for_day(date)
    
    # Initialize and run dashboard
    dashboard = Dashboard(db_manager.cursor)
    dashboard.run()

    db_manager.close()

if __name__ == "__main__":
    main()