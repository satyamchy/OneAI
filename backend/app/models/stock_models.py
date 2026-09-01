import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from app.database import Base


class StockAnalysisSnapshot(Base):
    __tablename__ = "stock_analysis_snapshots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(50), index=True, nullable=False)
    symbol = Column(String(50), index=True, nullable=False)
    name = Column(String(100), nullable=True)
    initial_price = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    overall_sentiment = Column(String(30), default="Neutral")
    intraday_bias = Column(String(30), default="Neutral")
    period_return_pct = Column(Float, nullable=True)
    technical_score = Column(Float, nullable=True)
    structured_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(50), unique=True, index=True, nullable=False)
    symbol = Column(String(50), nullable=False)
    name = Column(String(100), nullable=True)
    added_at = Column(DateTime, default=datetime.datetime.utcnow)
