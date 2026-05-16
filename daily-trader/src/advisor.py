"""
advisor.py
----------
🔵 DAUGHTER'S FILE

This module sends the signal data to the Claude AI API and gets back
plain-English daily trading advice.

It loads the prompt template from config/prompt_template.txt,
fills in today's signal data, and calls Claude.
"""

import anthropic
import os
import json
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads the .env file to get ANTHROPIC_API_KEY


def load_prompt_template() -> str:
    """Load the AI prompt template that Dad wrote."""
    prompt_path = Path(__file__).parent.parent / "config" / "prompt_template.txt"
    with open(prompt_path) as f:
        return f.read()


def format_signals_for_prompt(signals: list[dict]) -> str:
    """
    Convert the signals list into a readable text block for the AI prompt.

    Example output:
        AAPL  | Close: $182.50 | RSI: 45.1 (neutral)   | MACD: bullish | MA Cross: golden  | Overall: bullish
        SPY   | Close: $445.20 | RSI: 62.3 (neutral)   | MACD: bullish | MA Cross: golden  | Overall: bullish
    """
    lines = []
    for s in signals:
        line = (
            f"{s['ticker']:6} | Close: ${s['latest_close']:8.2f} | "
            f"RSI: {s['rsi']:5.1f} ({s['rsi_signal']:10}) | "
            f"MACD: {s['macd_signal']:8} | MA Cross: {s['ma_cross']:7} | "
            f"Overall: {s['overall']}"
        )
        lines.append(line)
    return "\n".join(lines)


def get_daily_advice(signals: list[dict]) -> str:
    """
    Send today's signals to Claude and return the advice text.

    Args:
        signals: list of signal dicts from signals.calculate_all_signals()

    Returns:
        A string containing today's plain-English advice
    """
    template = load_prompt_template()
    signals_text = format_signals_for_prompt(signals)
    today = date.today().strftime("%A, %B %d %Y")

    # Fill in the template placeholders
    full_prompt = template.replace("{{DATE}}", today)
    full_prompt = full_prompt.replace("{{SIGNALS}}", signals_text)

    # Call the Claude API
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )

    return message.content[0].text


if __name__ == "__main__":
    # Run this file directly to test: python src/advisor.py
    from data_fetcher import load_watchlist, fetch_price_history
    from signals import calculate_all_signals

    print("Running full advice pipeline...\n")
    tickers = load_watchlist()
    price_data = fetch_price_history(tickers)
    signals = calculate_all_signals(price_data)

    print("Asking Claude for advice...\n")
    advice = get_daily_advice(signals)

    print("=" * 60)
    print("TODAY'S ADVICE")
    print("=" * 60)
    print(advice)
