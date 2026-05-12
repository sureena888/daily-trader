# 📈 Daily Trading Advisor App — Project Plan

A father-daughter project to build a mobile app that delivers daily stock & ETF advice via push notification and SMS, powered by Python, technical analysis signals, and AI.

---

## How This Plan Works

Tasks are labelled by who should lead them:

- 🟢 **Dad** — no prior coding experience needed; focuses on content, config, and testing
- 🔵 **Daughter** — uses CS skills to build the technical plumbing
- 🟡 **Together** — pair-program or review each other's work

---

## Phase 1 — Set Up the Workspace

**Goal:** Get your computers ready to run Python code.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 1.1 | Install Python | 🟢 Dad | Download Python 3.11+ from python.org and install it |
| 1.2 | Install VS Code | 🟢 Dad | Download from code.visualstudio.com — this is where you'll write and read code |
| 1.3 | Create the project folder | 🟡 Together | Make a folder called `daily-trader` on your computer |
| 1.4 | Set up a virtual environment | 🔵 Daughter | Run `python -m venv venv` inside the project folder, then `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows) |
| 1.5 | Install Python packages | 🔵 Daughter | Run `pip install yfinance pandas ta anthropic twilio python-dotenv schedule` |
| 1.6 | Create a GitHub repo | 🔵 Daughter | Create a private GitHub repo so you can both commit code and see each other's changes |

**Dad's learning moment:** A "virtual environment" is like a clean room for your project — it keeps its tools separate from everything else on your computer.

---

## Phase 2 — Build the Data Pipeline

**Goal:** Fetch real stock and ETF market data automatically every morning.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 2.1 | Write the watchlist | 🟢 Dad | Edit `config/watchlist.yaml` — add the tickers (e.g. AAPL, SPY) you want advice on. A starter file is provided. |
| 2.2 | Write the data fetcher | 🔵 Daughter | `src/data_fetcher.py` — uses `yfinance` to download the last 60 days of price data for each ticker in the watchlist |
| 2.3 | Test the data fetcher | 🟡 Together | Dad runs `python src/data_fetcher.py` and checks the output looks right |

**Dad's learning moment:** A "ticker" is the short code for a stock — AAPL = Apple, SPY = S&P 500 ETF.

---

## Phase 3 — Calculate Trading Signals

**Goal:** Run basic technical analysis on the price data to spot patterns.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 3.1 | Write the signals module | 🔵 Daughter | `src/signals.py` — calculates RSI, MACD, and 50-day vs 200-day moving average for each ticker |
| 3.2 | Add signal thresholds to config | 🟢 Dad | Edit `config/settings.yaml` — set what RSI level counts as "oversold" or "overbought". Guidance is in the file. |
| 3.3 | Test signals output | 🟡 Together | Run `python src/signals.py` — Dad reads the output and asks: does this match what you'd expect? |

**Dad's learning moment:** RSI (Relative Strength Index) is a number between 0–100. Below 30 usually means a stock may be oversold (potentially a buy signal). Above 70 may mean overbought (potential sell signal).

---

## Phase 4 — Generate AI Advice

**Goal:** Send the signals to Claude AI and get back plain-English daily advice.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 4.1 | Get a Claude API key | 🟢 Dad | Sign up at console.anthropic.com, create an API key, paste it into the `.env` file |
| 4.2 | Customise the AI prompt | 🟢 Dad | Edit `config/prompt_template.txt` — this is the instruction you give to the AI each morning. Personalise your risk tolerance, goals, and tone. |
| 4.3 | Write the AI advisor module | 🔵 Daughter | `src/advisor.py` — loads the prompt template, fills in the signal data, calls the Claude API, and returns the advice text |
| 4.4 | Test the advisor | 🟡 Together | Run `python src/advisor.py` — read the AI's advice out loud together. Does it make sense? Tweak the prompt if not. |

**Dad's learning moment:** The prompt is like a briefing note you hand to a very knowledgeable analyst every morning. The clearer and more specific it is, the better the advice.

---

## Phase 5 — Send Notifications

**Goal:** Deliver the daily advice to your phones automatically.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 5.1 | Set up Twilio | 🟢 Dad | Sign up at twilio.com (free trial), get a phone number, copy the Account SID and Auth Token into `.env` |
| 5.2 | Add phone numbers to config | 🟢 Dad | Edit `config/settings.yaml` — add your and your daughter's mobile numbers |
| 5.3 | Write the notifier module | 🔵 Daughter | `src/notifier.py` — sends the advice text as an SMS via Twilio |
| 5.4 | Write the daily scheduler | 🔵 Daughter | `src/scheduler.py` — ties everything together and runs the full pipeline at a set time each morning (e.g. 7:30 AM) |
| 5.5 | Test end-to-end | 🟡 Together | Run `python src/scheduler.py --now` to trigger immediately and check both phones receive the SMS |

---

## Phase 6 — Build the Mobile App

**Goal:** A simple React Native app where you can view the daily advice, your watchlist, and signal history.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 6.1 | Install Expo | 🔵 Daughter | `npm install -g expo-cli`, then `npx create-expo-app DailyTrader` |
| 6.2 | Build the home screen | 🔵 Daughter | `app/screens/HomeScreen.js` — displays today's AI advice and a list of signal summaries per ticker |
| 6.3 | Build the watchlist screen | 🟡 Together | `app/screens/WatchlistScreen.js` — shows each ticker with a green/amber/red signal badge |
| 6.4 | Connect app to backend | 🔵 Daughter | Add a simple FastAPI endpoint (`src/api.py`) that the mobile app calls to fetch today's advice |
| 6.5 | Add push notifications | 🔵 Daughter | Use Expo Notifications — register the device token and send a push each morning alongside the SMS |
| 6.6 | Test on both phones | 🟡 Together | Install Expo Go on both phones and run the app — Dad gives feedback on what's confusing or unclear |

---

## Phase 7 — Polish & Make It Yours

**Goal:** Personalise the app and make it feel finished.

| # | Task | Who | What to do |
|---|------|-----|-----------|
| 7.1 | Name and brand the app | 🟢 Dad | Pick a name, choose a colour theme — Daughter implements it |
| 7.2 | Add a disclaimer | 🟢 Dad | Write a note in the app that this is for educational purposes, not financial advice |
| 7.3 | Add a "Why?" explanation | 🟡 Together | For each signal, show a one-line plain English explanation of what it means |
| 7.4 | Write a README | 🟡 Together | Document how to run the project — great practice for Daughter, and Dad can write the non-technical intro |

---

## File Structure (what you'll build)

```
daily-trader/
│
├── config/
│   ├── watchlist.yaml        🟢 Dad edits this
│   ├── settings.yaml         🟢 Dad edits this
│   └── prompt_template.txt   🟢 Dad edits this
│
├── src/
│   ├── data_fetcher.py       🔵 Daughter builds this
│   ├── signals.py            🔵 Daughter builds this
│   ├── advisor.py            🔵 Daughter builds this
│   ├── notifier.py           🔵 Daughter builds this
│   ├── scheduler.py          🔵 Daughter builds this
│   └── api.py                🔵 Daughter builds this
│
├── app/                      🔵 Daughter builds this (React Native)
│   └── screens/
│       ├── HomeScreen.js
│       └── WatchlistScreen.js
│
├── .env                      🔒 Secret keys — NEVER share or commit this
├── requirements.txt          🔵 Daughter maintains this
└── README.md                 🟡 Write together
```

---

## Suggested Order of Play

**Week 1:** Phases 1–2 (setup + data)
**Week 2:** Phases 3–4 (signals + AI advice)
**Week 3:** Phase 5 (SMS notifications — this is where it gets exciting!)
**Week 4+:** Phase 6 (mobile app)
**Ongoing:** Phase 7 (make it your own)

---

## Key Concepts for Dad (Plain English Glossary)

| Term | What it means |
|------|--------------|
| **Ticker** | Short code for a stock or ETF (e.g. AAPL = Apple) |
| **ETF** | A fund that tracks a basket of stocks (e.g. SPY tracks the S&P 500) |
| **RSI** | A 0–100 score measuring if a stock is overbought or oversold |
| **MACD** | A signal that shows momentum — is the stock gaining or losing speed? |
| **Moving Average** | The average price over a period (e.g. last 50 days) — smooths out daily noise |
| **API** | A way for two programs to talk to each other |
| **Virtual environment** | An isolated Python workspace so packages don't clash |
| **.env file** | A private file holding secret keys — never share this |
| **Cron / Scheduler** | A timer that runs your script automatically at a set time |

---

*This is a learning project. Nothing in this app constitutes financial advice. Always do your own research before making investment decisions.*
