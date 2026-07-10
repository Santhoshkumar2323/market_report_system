from sqlalchemy import Column, Integer, String, Float, Date, Text, Boolean
from modules.database import Base


class RawMarketData(Base):
    __tablename__ = "raw_market_data"

    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(Date)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class ProcessedMetrics(Base):
    __tablename__ = "processed_metrics"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)            # display name
    category = Column(String)          # Global Indices, US Sectors, etc.
    region = Column(String, nullable=True)  # United States, Europe, etc.

    latest_close = Column(Float)
    pct_change_1d = Column(Float)
    pct_change_5d = Column(Float)
    pct_change_10d = Column(Float)
    volatility_10d = Column(Float)

    high_10d = Column(Float)
    low_10d = Column(Float)

    week_timestamp = Column(Date)


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True)
    report_timestamp = Column(Date)
    structured_input_json = Column(Text)
    gemini_response_text = Column(Text)
    email_sent = Column(Boolean)


class EmailLog(Base):
    __tablename__ = "email_log"

    id = Column(Integer, primary_key=True)
    report_id = Column(Integer)
    recipient = Column(String)
    status = Column(String)
    error_message = Column(Text)