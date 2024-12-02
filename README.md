# Hedgineer Index

A Python-based system for creating and managing a custom stock market index that tracks top companies by market capitalization.

## Overview

Hedgineer Index is a tool that:
- Fetches real-time stock data from NASDAQ
- Calculates a custom index based on the top K stocks by market capitalization 
- Stores historical index data and compositions
- Provides an interface to query index values for specific dates
- Visualizes index performance through an interactive dashboard

## Features

- **Dynamic Stock Universe**: Automatically fetches top US stocks from NASDAQ API
- **Historical Data**: Maintains historical price and market cap data using Yahoo Finance
- **Split Adjusted**: Handles stock splits automatically for accurate historical calculations
- **In-Memory Database**: Uses SQLite for efficient data storage and retrieval
- **Interactive Dashboard**: Built with Streamlit for real-time visualization
- **Automated Updates**: Daily recalculation of index values and constituents

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- yfinance >= 0.2.0
- streamlit >= 1.40.0
- requests >= 2.32.0
- sqlite3 (included in Python standard library)

## Installation

1. Clone the repository:

2. Create and activate a virtual environment (recommended):

### On Windows
```
python -m venv venv
.\venv\Scripts\activate
```
### On macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit dashboard:
```bash
streamlit run app.py
```

2. The dashboard will automatically:
- Fetch current market data
- Calculate index values
- Display interactive visualizations
- Show index constituents and performance metrics

## Project Structure

```
hedgineer-index/
├── app.py                 # Main application entry point
├── src/
│   ├── data/             # Data fetching and storage
│   ├── index/            # Index calculation logic
│   └── visualization/    # Dashboard and plotting
├── constants.py          # Configuration constants
└── requirements.txt      # Project dependencies
```

## Dashboard
![screencapture-localhost-8501-2024-12-02-22_13_37](https://github.com/user-attachments/assets/27cc6c95-9938-47b6-8004-a101ca40a11b)

