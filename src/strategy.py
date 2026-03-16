# strategy.py
import math
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List
from indicators import ema, sma, rsi, macd, atr, stoch, volume_zscore

from parameters import (
    RSI_GOOD_LOW,
    RSI_GOOD_HIGH,
    RSI_WEAK,
    RSI_OVERBOUGHT,
    PULLBACK_MIN,
    PULLBACK_MAX,
    EXTENDED_ABOVE_EMA,
    EXTENDED_BELOW_EMA,
    VOLUME_Z_BREAKOUT,
    ATR_MIN,
    ATR_MAX,
    ATR_LOW,
    MIN_DOLLAR_VOLUME,
    RR_STRONG,
    RR_GOOD,
    ACCOUNT_SIZE,
    RISK_PER_TRADE,
)

@dataclass
class Scores:
    """Container for a ticker's buy score, sell urgency, and reasoning notes."""
    buy_score: float
    sell_urgency: float
    notes: List[str]


def grade_row(df: pd.DataFrame) -> Scores:
    """
    Score the most recent row of a feature-enriched DataFrame.

    Scoring breakdown (max 100):
      Trend       0–30   (price above key MAs, MACD direction)
      Momentum    0–25   (RSI zone, pullback to EMA20)
      Breakout    0–20   (new 20-day high, volume confirmation)
      Volatility  0–10   (ATR% in tradeable range)
      Liquidity  -10–10  (avg daily dollar volume)
      Risk/Reward 0–15   (reward-to-risk ratio)
    """
    notes = []
    row = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else row
    close = row["Close"]

    # --- Trend (0–30) ---
    trend = 0
    if close > row["SMA50"]:
        trend += 8
        notes.append("Close>SMA50")
    if row["SMA20"] > row["SMA50"]:
        trend += 8
        notes.append("SMA20>SMA50")
    if row["MACD"] > 0:
        trend += 7
        notes.append("MACD>0")
    if row["MACD_HIST"] > 0 and prev["MACD_HIST"] <= 0:
        trend += 7
        notes.append("MACD bullish turn")

    # --- Momentum / Pullback (0–25) ---
    momentum = 0
    rsi_val = row["RSI14"]
    pull = (close - row["EMA20"]) / row["EMA20"]  # % distance from EMA20

    if RSI_GOOD_LOW <= rsi_val <= RSI_GOOD_HIGH:
        momentum += 10
        notes.append(f"RSI healthy ({RSI_GOOD_LOW}–{RSI_GOOD_HIGH})")
    elif rsi_val < RSI_WEAK:
        momentum -= 5
        notes.append(f"RSI weak (<{RSI_WEAK})")

    if PULLBACK_MIN <= pull <= PULLBACK_MAX:
        momentum += 10
        notes.append("Pullback to EMA20")
    elif pull > EXTENDED_ABOVE_EMA:
        momentum -= 5
        notes.append("Extended above EMA20")

    # --- Breakout (0–20) ---
    breakout = 0
    if close >= row["HH20"] and row["VOL_Z"] > VOLUME_Z_BREAKOUT:
        breakout += 15
        notes.append("20D high + volume surge")
    elif close >= row["HH20"]:
        breakout += 8
        notes.append("20D high")

    # --- Volatility fit (0–10) ---
    atr_pct = row["ATR14"] / close
    vol_score = 0

    if ATR_MIN <= atr_pct <= ATR_MAX:
        vol_score += 8
        notes.append("ATR% in sweet spot")
    elif atr_pct < ATR_LOW:
        vol_score += 2
        notes.append("Very quiet")
    else:
        vol_score += 3
        notes.append("Volatile")

    # --- Liquidity (-10 to +10) ---
    liquidity = 10 if row["DollarVol20"] >= MIN_DOLLAR_VOLUME else -10
    notes.append(
        f"Liquid (≥${MIN_DOLLAR_VOLUME:,.0f})"
        if liquidity > 0
        else f"Low liquidity (<${MIN_DOLLAR_VOLUME:,.0f})"
    )

    # --- Risk / Reward (0–15) ---
    # Stop = higher of 10-day low OR 3% below EMA20
    stop = max(row["LL10"], row["EMA20"] * 0.97)
    target = max(row["HH10"], close + 2 * row["ATR14"])
    risk = close - stop
    reward = target - close
    rr = reward / (risk + 1e-9)

    rr_score = 0
    if rr >= RR_STRONG:
        rr_score += 15
        notes.append(f"R:R≥{RR_STRONG} ({rr:.1f})")
    elif rr >= RR_GOOD:
        rr_score += 10
        notes.append(f"R:R≥{RR_GOOD} ({rr:.1f})")
    else:
        rr_score += 2
        notes.append(f"R:R thin ({rr:.1f})")

    buy_score = max(
        0,
        min(100, trend + momentum + breakout + vol_score + liquidity + rr_score)
    )

    # --- Sell urgency (0–100) ---
    sell = 0
    if rsi_val > RSI_OVERBOUGHT:
        sell += 20
        notes.append(f"Overbought RSI>{RSI_OVERBOUGHT}")
    if row["MACD_HIST"] < 0 and prev["MACD_HIST"] >= 0:
        sell += 25
        notes.append("MACD bearish turn")
    if close < row["EMA20"]:
        sell += 20
        notes.append("Close<EMA20")
    if close < stop:
        sell += 35
        notes.append("Broke stop")
    if pull < EXTENDED_BELOW_EMA:
        sell += 10
        notes.append("Extended below EMA20")

    return Scores(buy_score, sell, notes)

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add all technical indicator columns to a raw OHLCV DataFrame."""
    out = df.copy()

    # Moving averages
    out["EMA20"] = ema(out["Close"], 20)
    out["SMA20"] = sma(out["Close"], 20)
    out["SMA50"] = sma(out["Close"], 50)

    # Momentum indicators
    out["RSI14"] = rsi(out["Close"], 14)
    out["MACD"], out["MACD_SIG"], out["MACD_HIST"] = macd(out["Close"])

    # Volatility
    out["ATR14"] = atr(out, 14)
    out["STOCHK"], out["STOCHD"] = stoch(out, 14, 3)

    # Price range lookbacks
    out["HH10"] = out["High"].rolling(10).max()   # 10-day high
    out["LL10"] = out["Low"].rolling(10).min()    # 10-day low
    out["HH20"] = out["High"].rolling(20).max()   # 20-day high

    # Volume
    out["VOL_Z"]      = volume_zscore(out["Volume"], 20)
    out["DollarVol20"] = (out["Close"] * out["Volume"]).rolling(20).mean()

    return out.dropna()

# Position Sizing
def position_size(entry, stop, account=ACCOUNT_SIZE, risk_pct=RISK_PER_TRADE) -> int:
    """
    Calculate how many shares to buy based on a fixed-risk model.
    Example: $6,000 account, 1% risk → risk $60 per trade.
    If stop is $2 below entry, buy 30 shares.
    """
    risk_dollars   = account * risk_pct
    per_share_risk = max(0.01, entry - stop)  # floor at 1 cent to avoid divide-by-zero
    return max(0, math.floor(risk_dollars / per_share_risk))

def run_prefetched(price_cache: dict, account: float, risk_pct: float) -> pd.DataFrame:
    """
    Score every ticker in the price cache and return a sorted DataFrame.
    Tickers that raise an error are included with zeroed scores and an error note.
    """
    rows = []

    for ticker, raw in price_cache.items():
        try:
            df    = compute_features(raw)
            sc    = grade_row(df)
            last  = df.iloc[-1]
            close = float(last["Close"])
            stop  = float(max(last["LL10"], last["EMA20"] * 0.97)) #0.97 is ~3% below EMA20. This sets a stop roughly 3% below the 20-day EMA
            target = float(max(last["HH10"], close + 2 * last["ATR14"])) #2x ATR indicates a strong mover
            rr    = (target - close) / (close - stop + 1e-9)

            row = {
                "Ticker":          ticker,
                "Date":            df.index[-1].date().isoformat(),
                "Close":           round(close, 2),
                "BuyScore":        round(sc.buy_score, 1),
                "SellUrgency":     round(sc.sell_urgency, 1),
                "RSI14":           round(float(last["RSI14"]), 1),
                "ATR%":            round(float(last["ATR14"] / close) * 100, 2),
                "Stop":            round(stop, 2),
                "Target":          round(target, 2),
                "R_Ratio":         round(rr, 2),
                "SuggestedShares": position_size(close, stop, account, risk_pct),
                "Notes":           " | ".join(sc.notes),
            }
        except Exception as e:
            row = {
                "Ticker": ticker, "Date": "", "Close": np.nan,
                "BuyScore": 0, "SellUrgency": 0, "RSI14": np.nan,
                "ATR%": np.nan, "Stop": np.nan, "Target": np.nan,
                "R_Ratio": np.nan, "SuggestedShares": 0,
                "Notes": f"Error: {e}",
            }

        rows.append(row)

    df_out = pd.DataFrame(rows)
    if {"BuyScore", "SellUrgency"}.issubset(df_out.columns):
        df_out = df_out.sort_values(
            ["BuyScore", "SellUrgency"], ascending=[False, True]
        ).reset_index(drop=True)

    return df_out
