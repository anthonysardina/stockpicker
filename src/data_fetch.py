# data_fetch.py -> Data Fetching

import pandas as pd
import yfinance as yf

def fetch(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Download OHLCV data for a single ticker via yfinance.
    Handles MultiIndex columns and 'Adj Close' naming variants.
    Returns a clean DataFrame with columns: Open, High, Low, Close, Volume.
    """
    df = yf.download(ticker, period=period, interval=interval,
                     auto_adjust=True, progress=False)

    if df is None or df.empty:
        raise ValueError(f"No data returned for {ticker}.")

    # yfinance sometimes returns MultiIndex columns like ('Close', 'AAPL')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
        df = df.loc[:, ~pd.Index(df.columns).duplicated()]

    # Rename 'Adj Close' → 'Close' if needed
    if "Close" not in df.columns and "Adj Close" in df.columns:
        df = df.rename(columns={"Adj Close": "Close"})

    # Keep only the five standard OHLCV columns
    ohlcv = ["Open", "High", "Low", "Close", "Volume"]
    df = df[[c for c in ohlcv if c in df.columns]].copy()

    # Coerce every column to numeric and drop rows with missing values
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()

    if df.empty or df["Close"].isna().all():
        raise ValueError(f"No usable price data for {ticker}.")

    return df

def _clean_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize a raw yfinance slice to standard float OHLCV columns."""
    if "Close" not in df.columns and "Adj Close" in df.columns:
        df = df.rename(columns={"Adj Close": "Close"})
    keep = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
    out  = df[keep].copy()
    for col in out.columns:
        if isinstance(out[col], pd.DataFrame):   # squeeze accidental 2-D columns
            out[col] = out[col].iloc[:, 0]
        out[col] = pd.to_numeric(out[col], errors="coerce")
    return out.dropna()


def prefetch_prices(tickers: list, period: str = "6mo", interval: str = "1d") -> dict:
    """
    Download price data for many tickers in a single Yahoo Finance call.
    Returns a dict of {ticker: OHLCV DataFrame}.
    Tickers that return no data are silently skipped.
    """
    if not tickers:
        return {}

    data = yf.download(
        tickers, period=period, interval=interval,
        auto_adjust=True, progress=False,
        group_by="ticker", threads=True,
    )

    cache = {}

    if isinstance(data.columns, pd.MultiIndex):
        # Multi-ticker response: columns are (ticker, field)
        available = sorted({col[0] for col in data.columns})
        for t in tickers:
            if t in available:
                try:
                    sub = _clean_ohlcv(data[t])
                    if not sub.empty and sub["Close"].notna().any():
                        cache[t] = sub
                except Exception:
                    pass
    else:
        # Single-ticker fallback
        sub = _clean_ohlcv(data)
        if not sub.empty:
            cache[tickers[0]] = sub

    return cache

