import requests
import pandas as pd
from datetime import datetime, timedelta
from config.settings import settings
import time

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred_series(series_id, days=400, retries=3):

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    params = {
        "series_id": series_id,
        "api_key": settings.FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    for attempt in range(retries):

        try:
            response = requests.get(FRED_URL, params=params, timeout=15)
            response.raise_for_status()

            data = response.json().get("observations", [])

            df = pd.DataFrame(data)

            if df.empty:
                return pd.DataFrame()

            df["date"] = pd.to_datetime(df["date"])
            df["value"] = pd.to_numeric(df["value"], errors="coerce")

            df = df.dropna(subset=["value"])
            df = df.sort_values("date")

            return df

        except Exception as e:

            wait = 2 ** attempt
            print(f"FRED fetch error {series_id} attempt {attempt+1}: {e}")
            time.sleep(wait)

    # -------- fallback smaller query --------
    try:

        print(f"FRED fallback query for {series_id}")

        params["observation_start"] = end_date - timedelta(days=120)

        response = requests.get(FRED_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json().get("observations", [])

        df = pd.DataFrame(data)

        if df.empty:
            return pd.DataFrame()

        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        df = df.dropna(subset=["value"])
        df = df.sort_values("date")

        return df

    except Exception as e:

        print(f"FRED final failure {series_id}: {e}")

        return pd.DataFrame()