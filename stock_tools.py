import os
import yfinance as yf
from crewai.tools import tool

@tool("Fetch Indian Stock Data")
def fetch_stock_data(ticker: str, period: str = "6mo") -> str:
    """
    Fetches historical daily stock data for a given Indian ticker from Yahoo Finance.
    The ticker must end with '.NS' for NSE (e.g., 'TCS.NS', 'RELIANCE.NS').
    Period options include: '1mo', '3mo', '6mo', '1y'.
    """
    try:
        # Ensure the ticker has the proper NSE suffix if missing
        if not ticker.endswith('.NS') and not ticker.endswith('.BO'):
            ticker = f"{ticker}.NS"
            
        # Quick fix for Yahoo Finance period naming quirks
        if period == "6m": period = "6mo"
        if period == "3m": period = "3mo"
        if period == "1m": period = "1mo"
            
        print(f"\n[Tool] Fetching data for {ticker} over the last {period}...")
        
        # Download data
        data = yf.download(ticker, period=period, interval="1d")
        
        if data.empty:
            return f"Error: No data found for ticker {ticker}."
            
        # Save to your data folder
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{ticker}_data.csv"
        data.to_csv(file_path)
        
        # Bulletproof fix for Yahoo Finance's multi-level column structure
        close_values = data['Close'].values.flatten()
        latest_price = float(close_values[-1])
        
        return f"Success! Saved {len(data)} days of data to '{file_path}'. Latest closing price for {ticker}: INR {latest_price:.2f}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"