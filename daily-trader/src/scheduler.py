"""
scheduler.py
------------
🔵 DAUGHTER'S FILE

This is the main entry point that ties everything together.
It runs the full pipeline:
  1. Fetch price data
  2. Calculate signals
  3. Get AI advice
  4. Send SMS notifications

You can either:
  - Run it immediately:  python src/scheduler.py --now
  - Schedule it daily:   python src/scheduler.py
    (keeps running and fires at the time set in settings.yaml)
"""

import sys
import schedule
import time
import yaml
from pathlib import Path
from datetime import datetime

# Import our own modules
from data_fetcher import load_watchlist, fetch_price_history
from signals import calculate_all_signals
from advisor import get_daily_advice
from notifier import send_sms, get_recipients_from_env


def load_settings() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def run_daily_pipeline():
    """
    The full morning pipeline: fetch → signals → AI advice → send SMS.
    """
    print(f"\n{'='*60}")
    print(f"Daily Trader — {datetime.now().strftime('%A %B %d, %Y at %H:%M')}")
    print(f"{'='*60}\n")

    # Step 1: Load watchlist and fetch prices
    print("📥 Step 1: Fetching price data...")
    tickers = load_watchlist()
    price_data = fetch_price_history(tickers)

    if not price_data:
        print("❌ No price data fetched. Aborting.")
        return

    # Step 2: Calculate signals
    print("\n📊 Step 2: Calculating signals...")
    signals = calculate_all_signals(price_data)

    # Step 3: Get AI advice
    print("\n🤖 Step 3: Asking Claude for today's advice...")
    advice = get_daily_advice(signals)
    print("\nToday's advice:\n")
    print(advice)

    # Step 4: Send SMS
    print("\n📱 Step 4: Sending SMS notifications...")
    recipients = get_recipients_from_env()
    if recipients:
        # Trim advice to fit SMS limits if needed
        sms_message = f"📈 Daily Trader — {datetime.now().strftime('%b %d')}\n\n{advice[:1400]}"
        send_sms(sms_message, recipients)
    else:
        print("  ⚠️  No recipients configured in .env (RECIPIENT_PHONES)")

    print("\n✅ Done!\n")


if __name__ == "__main__":
    settings = load_settings()
    run_time = settings.get("schedule", {}).get("run_at", "07:30")

    # If --now flag is passed, run immediately
    if "--now" in sys.argv:
        print("Running pipeline immediately (--now flag detected)...")
        run_daily_pipeline()
    else:
        print(f"Scheduler started. Pipeline will run daily at {run_time}.")
        print("Press Ctrl+C to stop.\n")
        schedule.every().day.at(run_time).do(run_daily_pipeline)
        while True:
            schedule.run_pending()
            time.sleep(60)
