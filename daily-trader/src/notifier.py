"""
notifier.py
-----------
🔵 DAUGHTER'S FILE

This module sends the daily advice as an SMS using Twilio.
It reads phone numbers and Twilio credentials from the .env file.

Sign up for a free Twilio account at: https://www.twilio.com
You'll get a trial phone number and some free credits to get started.
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


def send_sms(message: str, recipients: list[str]) -> None:
    """
    Send an SMS message to one or more phone numbers.

    Args:
        message: The text to send (keep under 1600 chars for a single SMS)
        recipients: List of phone numbers in E.164 format, e.g. ["+14155552671"]
    """
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    from_number = os.environ["TWILIO_PHONE_NUMBER"]

    client = Client(account_sid, auth_token)

    for phone_number in recipients:
        try:
            msg = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            print(f"  ✅ SMS sent to {phone_number} (SID: {msg.sid})")
        except Exception as e:
            print(f"  ❌ Failed to send SMS to {phone_number}: {e}")


def get_recipients_from_env() -> list[str]:
    """
    Read the comma-separated list of phone numbers from .env.
    Example in .env: RECIPIENT_PHONES=+14155552671,+14155559876
    """
    raw = os.environ.get("RECIPIENT_PHONES", "")
    return [p.strip() for p in raw.split(",") if p.strip()]


if __name__ == "__main__":
    # Run this file directly to test: python src/notifier.py
    print("Sending a test SMS...")
    recipients = get_recipients_from_env()
    if not recipients:
        print("No recipients found. Add RECIPIENT_PHONES to your .env file.")
    else:
        send_sms("🧪 Test message from your Daily Trader app! It's working.", recipients)
