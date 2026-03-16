# Parameters --> Change these values to adjust the grading calculations in strategy.py

# RSI thresholds
RSI_GOOD_LOW = 50
RSI_GOOD_HIGH = 70
RSI_WEAK = 40
RSI_OVERBOUGHT = 70

# Pullback thresholds
PULLBACK_MIN = -0.03
PULLBACK_MAX = 0.00
EXTENDED_ABOVE_EMA = 0.06
EXTENDED_BELOW_EMA = -0.06

# Breakout
VOLUME_Z_BREAKOUT = 1.0

# Volatility
ATR_MIN = 0.01
ATR_MAX = 0.04
ATR_LOW = 0.008

# Liquidity
MIN_DOLLAR_VOLUME = 5_000_000

# Risk reward thresholds
RR_STRONG = 2.0
RR_GOOD = 1.5

# Personal risk and sizing
ACCOUNT_SIZE = 6000
RISK_PER_TRADE = 0.01

#Display Customizing
WATCHLIST_ROWS_TO_SHOW = None
OWNED_ROWS_TO_SHOW = 15