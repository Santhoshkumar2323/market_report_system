# market_report_system

A self-contained pipeline that fetches global market data, runs a signal engine, and delivers a formatted weekly macro report to email — fully automated.

Built with Python, PostgreSQL, yfinance, FRED API, and Gemini.

Sample output screenshots are in sample_output/

# What the report covers

Global equity indices — US, Europe, Japan, China, India with 10-day return and volatility

US and India sector breakdown — relative strength across sectors

Commodities and crypto — price and 10-day performance

Global bond market — 10Y/2Y yields, 3M and 6M deltas, yield curve shape for 6 countries

Liquidity and credit — Fed balance sheet, reverse repo, HY/IG spreads, real yields via FRED

Signal summary — strongest/weakest region, sector leadership, commodity and crypto signals, volatility state

AI commentary — Gemini 2.5 Flash interprets the signals into 5–8 bullet points

# How it works

# main.py runs three things in sequence:

Data pipeline — fetches 10 days of OHLCV data for every asset via yfinance, computes metrics (returns, volatility, highs/lows), and stores them in PostgreSQL. Deduplicates on re-run.

Report builder — pulls the latest snapshot from the DB, runs the signal engine, calls Gemini with only the derived signals (not raw prices), and assembles the full HTML email.

Email sender — sends via Gmail SMTP to all configured recipients and logs delivery status per recipient in the DB.

FRED data (bond yields, liquidity indicators) is fetched fresh at report time, not stored.


# Stack

LayerToolEquity, crypto, commodity OHLCV = yfinance

Bond yields + liquidity indicators = FRED API (St. Louis Fed)

Database = PostgreSQL + SQLAlchemy

AI commentary = Google Gemini 2.5 Flash

Email delivery = Gmail SMTP

# Setup

Install dependencies

pip install -r requirements.txt

Environment variables — create config/.env:

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_HOST=

POSTGRES_PORT=

POSTGRES_DB=

EMAIL_USER=

EMAIL_PASSWORD=          # Gmail App Password, not your login password

RECIPIENTS= a@x.com, b@x.com

FRED_API_KEY=            # free at fred.stlouisfed.org

GEMINI_API_KEY=          # free at aistudio.google.com

# Run

python main.py


# Caveats

# Data pipeline

yfinance is an unofficial API. It occasionally returns empty or malformed data for specific tickers 

The pipeline requires at least 10 days of OHLCV rows to compute metrics. If a ticker returns fewer, it is dropped without fallback.

FRED series have a retry + smaller-window fallback, but several series (e.g. monthly yield data) update infrequently — so 3M/6M deltas can reflect data that is a few weeks stale.

There is no alerting if a section fails. Yield table, macro table, and Gemini each fail silently and the email sends without them.


# Report logic

Deduplication is date-based. Running twice on the same day produces one DB record, but does not update it if the market moved — so intraday re-runs reflect the first fetch of the day.

Gemini commentary is derived from signals only (strongest region, sector, volatility state etc.), not from the underlying numbers. 

No dashboard or web UI. This is a scheduled email pipeline only.







