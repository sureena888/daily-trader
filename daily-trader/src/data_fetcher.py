"""
data_fetcher.py
---------------
🔵 DAUGHTER'S FILE

This module downloads recent price history for every ticker
in the watchlist using the free yfinance library.

It returns a dictionary: { "AAPL": <DataFrame>, "SPY": <DataFrame>, ... }
Each DataFrame has columns: Open, High, Low, Close, Volume
"""

import yfinance as yf
import yaml
from pathlib import Path


def load_watchlist() -> list[str]:
    """Read the list of tickers from config/watchlist.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "watchlist.yaml"
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return data["tickers"]


def fetch_price_history(tickers: list[str], period_days: int = 60) -> dict:
    """
    Download the last `period_days` days of daily price data for each ticker.

    Args:
        tickers: list of ticker symbols, e.g. ["AAPL", "SPY"]
        period_days: how many calendar days of history to fetch

    Returns:
        dict mapping each ticker to a pandas DataFrame of OHLCV data
    """
    results = {}
    period = f"{period_days}d"

    for ticker in tickers:
        print(f"  Fetching data for {ticker}...")
        try:
            df = yf.download(ticker, period=period, progress=False)
            if df.empty:
                print(f"  ⚠️  No data returned for {ticker} — skipping")
                continue
            results[ticker] = df
            print(f"  ✅ {ticker}: {len(df)} days of data")
        except Exception as e:
            print(f"  ❌ Error fetching {ticker}: {e}")

    return results


if __name__ == "__main__":
    # Run this file directly to test: python src/data_fetcher.py
    print("Loading watchlist...")
    tickers = load_watchlist()
    print(f"Tickers to track: {tickers}\n")

    print("Fetching price history...")
    data = fetch_price_history(tickers)

    print(f"\nDone! Fetched data for {len(data)} tickers.")
    for ticker, df in data.items():
        close_data = df["Close"]
        latest = close_data.iloc[-1, 0] if getattr(close_data, "ndim", 1) == 2 else close_data.iloc[-1]
        print(f"  {ticker}: latest close = ${float(latest):.2f}")
