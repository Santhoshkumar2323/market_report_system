# modules/data_fetcher.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_ticker_data(ticker: str) -> pd.DataFrame:
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=25)

        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            group_by="column",
            auto_adjust=False,
            threads=False,
        )

        if df.empty:
            return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

    
        required = ["Open", "High", "Low", "Close", "Volume"]
        for col in required:
            if col not in df.columns:
                return pd.DataFrame()

        df = df[required].dropna()
        df = df.tail(10)
        df.reset_index(inplace=True)
        return df

    except Exception as e:
        print(f"Fetch error {ticker}: {e}")
        return pd.DataFrame()