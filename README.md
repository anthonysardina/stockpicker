# StockPicker

A project by Anthony Sardina. October 2025.

## Overview:

This Python-based stock screening tool evaluates large sets of publicly traded equities using real-time technical data from Yahoo Finance. It computes a structured scoring model and returns ranked dataframes containing key trading signals such as BuyScore, SellUrgency, Risk Ratio, Target and Stop-loss prices, and other technical indicators. These figures can be used and interpreted by the user in order to make informed stock trading decisions.

------------------------------------------------------------------------

## Project Structure:

This project consists of 4 python scripts, each of which is responsible for a different function in the stock grading process, and 1 Jupyter Notebook file which is responsible for implementing the scripts and outputting data frames containing the stock sorted by categories of the user's choosing in order to make informed and calculated investing decisions.

-   `stockpicker.ipynb` - Main notebook: run this to fetch, score, and display results

-   `parameters.py` - All adjustable settings (thresholds, account size, risk %, etc...)

-   `tickers.py` - Watchlist, owned positions, aliases (tickers that have changed or go by more than one name), and sanitation logic

-   `indicators.py` - Technical indicator functions (EMA, SMA, RSI, MACD, ATR, etc.)

-   `data_fetch.py` - Yahoo Finance data fetching and OHLCV normalization

-   `strategy.py` - All scoring calculating and logic, position sizing, feature engineering

------------------------------------------------------------------------

## What It Does:

The notebook scans a list of ticker symbols and produces two ranked tables:

-   **Watchlist** - all stocks you want to monitor, sorted by "BuyScore" by default
-   **Owned** - stocks you currently hold, sorted by "SellUrgency" by default

For each ticker, it calculates a **BuyScore** (0-100) and a **SellUrgency** score (0-100), along with a suggested stop-loss price, target price, risk/reward ratio, and recommended share count based on your account size and risk level.

------------------------------------------------------------------------

## Scoring Algorithm:

Each ticker is evaluated on six independent factors. Scores are summed to produce the final BuyScore, capped between 0 and 100.

### 1. Trend (0-30 points)

Measures whether the stock is in an uptrend using moving averages and MACD.

| Condition                                               | Points |
|---------------------------------------------------------|--------|
| Close price is above the 50-day SMA                     | +8     |
| 20-day SMA is above the 50-day SMA                      | +8     |
| MACD line is positive                                   | +7     |
| MACD histogram just turned positive (bullish crossover) | +7     |

### 2. Momentum / Pullback (0-25 points)

Rewards stocks with healthy momentum and penalizes those that are overextended or weakening.

| Condition                                               | Points |
|---------------------------------------------------------|--------|
| RSI between 50 and 70 (strong but not overbought)       | +10    |
| Price has pulled back to within 3% below the 20-day EMA | +10    |
| RSI below 40 (weak momentum)                            | −5     |
| Price extended more than 6% above the 20-day EMA        | −5     |

### 3. Breakout (0-20 points)

Identifies stocks breaking out into new highs, with extra weight given when volume confirms the move.

| Condition                                                       | Points |
|-----------------------------------------------------------------|--------|
| Price at a 20-day high with above-average volume (Z-score \> 1) | +15    |
| Price at a 20-day high (no volume confirmation)                 | +8     |

### 4. Volatility Fit (0-10 points)

Targets stocks with a "tradeable" volatility range. This means they are somewhere in between too wild and too quite. ATR% is the Average True Range divided by price.

| Condition                           | Points |
|-------------------------------------|--------|
| ATR% between 1% and 4% (sweet spot) | +8     |
| ATR% below 0.8% (very quiet)        | +2     |
| ATR% above 4% (high volatility)     | +3     |

### 5. Liquidity (-10 to 10 points):

Filters out thinly traded stocks that are difficult to enter and exit cleanly.

| Condition                                     | Points |
|-----------------------------------------------|--------|
| 20-day average dollar volume ≥ \$5 million    | +10    |
| Below \$5 million average daily dollar volume | −10    |

### 6. Risk / Reward (0–15 points)

Calculates the ratio of potential reward to risk before entering a position. Stop is set at the higher of the 10-day low or 3% below the 20-day EMA. Target is set at the higher of the 10-day high or 2× ATR above the current price.

| Condition           | Points |
|---------------------|--------|
| R:R ratio ≥ 2.0     | +15    |
| R:R ratio ≥ 1.5     | +10    |
| R:R ratio below 1.5 | +2     |

------------------------------------------------------------------------

## Sell Urgency:

Similar to the BuyScore, the SellUrgency score is given to each stock as a number 0-100. It is based on five different scoring categories:

| Condition                                               | Points |
|---------------------------------------------------------|--------|
| Price breaks below the stop level                       | +35    |
| MACD histogram just turned negative (bearish crossover) | +25    |
| RSI above 70 (overbought)                               | +20    |
| Price falls below the 20-day EMA                        | +20    |
| Price extended more than 6% below the 20-day EMA        | +10    |

------------------------------------------------------------------------

## Position Sizing:

Share count is calculated using a fixed-risk model:

```         
risk_dollars   = account_size × per_trade_risk_pct
per_share_risk = entry_price − stop_price
suggested_shares = floor(risk_dollars / per_share_risk)
```

For example, with a \$6,000 account and 1% risk per trade (\$60), if the stop is \$2.00 below entry, the tool suggests 30 shares.

## Dependencies

```         
pip install yfinance pandas numpy jupyter
```

------------------------------------------------------------------------

## Configuration

All settings are in `src/parameters.py`. No changes to any other file are needed for basic use.

``` python
# Account & risk
ACCOUNT_SIZE     = 6000   # total account value in USD
RISK_PER_TRADE   = 0.01   # fraction of account to risk per trade (1% = $60)
 
# Display
WATCHLIST_ROWS_TO_SHOW = None   # None = show all rows
OWNED_ROWS_TO_SHOW     = 15
 
# Scoring thresholds (adjust to change what the algorithm rewards)
RSI_GOOD_LOW      = 50
RSI_GOOD_HIGH     = 70
RR_STRONG         = 2.0
MIN_DOLLAR_VOLUME = 5_000_000
# ...and more — all documented inline in parameters.py
```

To add or remove tickers, edit the `WATCHLIST` and `OWNED` lists in `src/tickers.py`.

------------------------------------------------------------------------

## Potential Future Improvements:

-   Add back-testing capability
-   integrate fundamental data (earnings, revenue growth)
-   Add portfolio optimization logic
-   Deploy as a web app or dashboard

------------------------------------------------------------------------

*This tool is for educational and informational purposes only. It is not financial advice. Always do your own research before making investment decisions.*