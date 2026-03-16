# indicators.py Technical Indicators  (no TA-Lib)

import numpy as np
import pandas as pd

def ema(series: pd.Series, span: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Relative Strength Index.
    Handles the edge case where yfinance returns a (n,1) DataFrame
    instead of a plain Series.
    """
    # Ensure we have a plain 1-D numeric Series
    s = series.iloc[:, 0] if isinstance(series, pd.DataFrame) else series
    s = pd.to_numeric(s, errors="coerce")

    delta = s.diff()
    gain = pd.Series(np.where(delta > 0, delta, 0.0), index=s.index)
    loss = pd.Series(np.where(delta < 0, -delta, 0.0), index=s.index)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / (avg_loss + 1e-12)  # tiny offset avoids division by zero
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD line, signal line, and histogram."""
    macd_line   = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram


def true_range(df: pd.DataFrame) -> pd.Series:
    """True Range: the largest of three candle-based spread measures."""
    prev_close = df["Close"].shift(1)
    return pd.concat([
        df["High"] - df["Low"],
        (df["High"] - prev_close).abs(),
        (df["Low"]  - prev_close).abs(),
    ], axis=1).max(axis=1)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range — measures how much a stock moves day-to-day."""
    return true_range(df).rolling(period).mean()


def stoch(df: pd.DataFrame, k_period: int = 14, d_period: int = 3):
    """Stochastic Oscillator (%K and %D lines)."""
    low_min  = df["Low"].rolling(k_period).min()
    high_max = df["High"].rolling(k_period).max()
    k = 100 * (df["Close"] - low_min) / (high_max - low_min + 1e-12)
    d = k.rolling(d_period).mean()
    return k, d


def volume_zscore(vol: pd.Series, window: int = 20) -> pd.Series:
    """How many standard deviations above/below average volume is today."""
    mean = vol.rolling(window).mean()
    std  = vol.rolling(window).std(ddof=0)
    return (vol - mean) / (std + 1e-12)