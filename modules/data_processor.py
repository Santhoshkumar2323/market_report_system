import numpy as np
from datetime import datetime, timezone
from sqlalchemy import and_
from modules.database import get_db_session
from modules.models import RawMarketData, ProcessedMetrics


def compute_metrics(df):
    if len(df) < 10:
        return None

    closes = df["Close"].astype(float)
    returns = closes.pct_change().dropna()

    return {
        "latest_close": float(closes.iloc[-1]),
        "pct_1d": float((closes.iloc[-1] / closes.iloc[-2] - 1) * 100),
        "pct_5d": float((closes.iloc[-1] / closes.iloc[-6] - 1) * 100),
        "pct_10d": float((closes.iloc[-1] / closes.iloc[0] - 1) * 100),
        "volatility_10d": float(np.std(returns) * np.sqrt(10) * 100),
        "high_10d": float(df["High"].max()),
        "low_10d": float(df["Low"].min()),
    }


def save_raw_data(session, ticker_symbol, df):
    for _, row in df.iterrows():
        exists = session.query(RawMarketData).filter(
            and_(
                RawMarketData.ticker == ticker_symbol,
                RawMarketData.date == row["Date"],
            )
        ).first()

        if exists:
            continue

        session.add(
            RawMarketData(
                ticker=ticker_symbol,
                date=row["Date"],
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            )
        )


def save_processed_metrics(session, display_name, category, region, metrics):
    week_date = datetime.now(timezone.utc).date()

    exists = session.query(ProcessedMetrics).filter(
        and_(
            ProcessedMetrics.ticker == display_name,
            ProcessedMetrics.week_timestamp == week_date,
        )
    ).first()

    if exists:
        return

    session.add(
        ProcessedMetrics(
            ticker=display_name,
            category=category,
            region=region,
            latest_close=metrics["latest_close"],
            pct_change_1d=metrics["pct_1d"],
            pct_change_5d=metrics["pct_5d"],
            pct_change_10d=metrics["pct_10d"],
            volatility_10d=metrics["volatility_10d"],
            high_10d=metrics["high_10d"],
            low_10d=metrics["low_10d"],
            week_timestamp=week_date,
        )
    )


def process_and_store(display_name, ticker_symbol, category, region, df):
    session = get_db_session()

    try:
        metrics = compute_metrics(df)
        if metrics is None:
            return

        save_raw_data(session, ticker_symbol, df)
        save_processed_metrics(session, display_name, category, region, metrics)

        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Processing error {ticker_symbol}: {e}")

    finally:
        session.close()