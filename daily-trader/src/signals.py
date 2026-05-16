"""
signals.py
----------
🔵 DAUGHTER'S FILE

This module takes the price data from data_fetcher.py and calculates
three technical indicators for each ticker:

  1. RSI  — Relative Strength Index (are buyers/sellers in control?)
  2. MACD — Moving Average Convergence/Divergence (is momentum shifting?)
  3. MA Cross — Is the 50-day average above or below the 200-day average?

It returns a summary dict for each ticker that the advisor.py module can read.
"""

import pandas as pd
import ta  # technical analysis library
import yaml
from pathlib import Path


def load_settings() -> dict:
    """Read signal threshold settings from config/settings.yaml."""
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def calculate_signals(ticker: str, df: pd.DataFrame, settings: dict) -> dict:
    """
    Calculate RSI, MACD, and moving average crossover for a single ticker.

    Args:
        ticker: e.g. "AAPL"
        df: DataFrame with at least a 'Close' column
        settings: dict from settings.yaml

    Returns:
        A dict summarising the signals, e.g.:
        {
          "ticker": "AAPL",
          "latest_close": 182.50,
          "rsi": 45.2,
          "rsi_signal": "neutral",       # "oversold", "neutral", "overbought"
          "macd_signal": "bullish",       # "bullish" or "bearish"
          "ma_cross": "golden",           # "golden" (bullish) or "death" (bearish) or "neutral"
          "overall": "mildly bullish"
        }
    """
    close = df["Close"].squeeze()

    # --- RSI ---
    rsi_indicator = ta.momentum.RSIIndicator(close=close, window=14)
    rsi = float(rsi_indicator.rsi().iloc[-1])

    rsi_oversold = settings["signals"]["rsi_oversold_threshold"]    # default: 30
    rsi_overbought = settings["signals"]["rsi_overbought_threshold"]  # default: 70

    if rsi < rsi_oversold:
        rsi_signal = "oversold"       # potential buy signal
    elif rsi > rsi_overbought:
        rsi_signal = "overbought"     # potential sell signal
    else:
        rsi_signal = "neutral"

    # --- MACD ---
    macd_indicator = ta.trend.MACD(close=close)
    macd_line = macd_indicator.macd().iloc[-1]
    signal_line = macd_indicator.macd_signal().iloc[-1]
    macd_signal = "bullish" if macd_line > signal_line else "bearish"

    # --- Moving Average Cross ---
    ma_cross = "neutral"
    if len(close) >= 200:
        ma50 = float(close.rolling(window=50).mean().iloc[-1])
        ma200 = float(close.rolling(window=200).mean().iloc[-1])
        if ma50 > ma200:
            ma_cross = "golden"    # 50-day above 200-day — bullish trend
        else:
            ma_cross = "death"     # 50-day below 200-day — bearish trend

    # --- Overall summary ---
    bullish_count = sum([
        rsi_signal == "oversold",
        macd_signal == "bullish",
        ma_cross == "golden"
    ])
    bearish_count = sum([
        rsi_signal == "overbought",
        macd_signal == "bearish",
        ma_cross == "death"
    ])

    if bullish_count >= 2:
        overall = "bullish"
    elif bearish_count >= 2:
        overall = "bearish"
    else:
        overall = "mixed / neutral"

    return {
        "ticker": ticker,
        "latest_close": round(float(close.iloc[-1]), 2),
        "rsi": round(rsi, 1),
        "rsi_signal": rsi_signal,
        "macd_signal": macd_signal,
        "ma_cross": ma_cross,
        "overall": overall
    }


def calculate_all_signals(price_data: dict) -> list[dict]:
    """
    Run calculate_signals() for every ticker in price_data.

    Args:
        price_data: dict from data_fetcher.fetch_price_history()

    Returns:
        List of signal summary dicts
    """
    settings = load_settings()
    all_signals = []
    for ticker, df in price_data.items():
        signals = calculate_signals(ticker, df, settings)
        all_signals.append(signals)
    return all_signals


if __name__ == "__main__":
    # Run this file directly to test: python src/signals.py
    from data_fetcher import load_watchlist, fetch_price_history

    print("Fetching price data...")
    tickers = load_watchlist()
    price_data = fetch_price_history(tickers)

    print("\nCalculating signals...\n")
    signals = calculate_all_signals(price_data)

    for s in signals:
        print(f"{s['ticker']:6} | Close: ${s['latest_close']:8.2f} | "
              f"RSI: {s['rsi']:5.1f} ({s['rsi_signal']:10}) | "
              f"MACD: {s['macd_signal']:8} | MA Cross: {s['ma_cross']:7} | "
              f"Overall: {s['overall']}")
