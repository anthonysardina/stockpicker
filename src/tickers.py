# tickers.py
WATCHLIST = [
    # Technology / Software
    "AAPL","MSFT","NVDA","AVGO","META","GOOGL","AMZN","TSLA","NFLX","CRM",
    "ADBE","ORCL","CSCO","INTC","AMD","QCOM","TXN","IBM","NOW","SHOP",
    "PLTR","UBER","DDOG","SNOW","CRWD","PANW","NET","ZS","MDB","TEAM",
    "DOCU","ZM","RBLX","ABNB","SPOT","ROKU","BIDU","PINS","TTD","TWLO",
    "BKNG","LYFT","DUOL","ARM","U","SNPS","CDNS","ANET","WDAY","ADSK",
    "FTNT","HUBS","MNDY","PATH","COIN","GFS","TSM","ASML","NTES",
    "BABA","TCEHY","SAP","WIX","IOT",

    # Semiconductors
    "AMAT","LRCX","KLAC","MU","MRVL","ON","NXPI","MCHP","MPWR",
    "WOLF","SWKS","QRVO","COHR","TER","ACLS","PLXS","NVMI",
    "AEHR","OLED","WDC","STX",

    # Financials
    "JPM","BAC","C","GS","MS","WFC","USB","PNC","TFC","COF","AXP",
    "MA","V","BLK","SCHW","SPGI","ICE","NDAQ","AON","MMC","CB",
    "PGR","TRV","AIG","MET","PRU","ALL","CME","ALLY","HOOD",

    # Healthcare / Biotech / Med-Tech
    "LLY","UNH","JNJ","MRK","ABBV","ABT","PFE","BMY","AMGN","GILD",
    "REGN","VRTX","BIIB","DHR","TMO","ISRG","MDT","SYK","BSX","EW",
    "HUM","CI","CVS","ZBH","GEHC","IDXX","DGX","LH","ILMN","HOLX",
    "DXCM","ALGN","ICUI","PODD","CRL","RMD","TDOC","NVCR","CRSP",
    "NTLA","BEAM","EXEL",

    # Industrials / Aerospace / Defense / Transport
    "GE","CAT","DE","HON","ETN","EMR","PCAR","CMI","IR","ITW","DOV",
    "AME","PH","ROK","TT","NDSN","BA","LMT","NOC","GD","RTX","TXT",
    "HWM","HEI","SPR","UPS","FDX","CHRW","ODFL","UNP","NSC","CSX",
    "CP","CNI","JBHT","LUV","DAL","AAL","UAL",

    # Energy
    "XOM","CVX","COP","SLB","HAL","BKR","OXY","EOG","DVN","FANG",
    "CTRA","APA","MPC","VLO","PSX","HESM","PBF","KMI","WMB","TRGP",
    "ET","ENB","EPD",

    # Materials / Chemicals / Miners
    "LIN","APD","ECL","SHW","PPG","DOW","DD","ALB","FCX","NUE",
    "STLD","AA","MLM","VMC","CF","MOS","FMC","BALL","SW","CE",
    "EMN","CTVA","LYB","RPM","GGB","VALE",

    # Consumer Discretionary
    "HD","LOW","NKE","MCD","SBUX","CMG","YUM","DRI","DPZ","SHAK",
    "TXRH","WING","WMT","COST","TGT","BBY","ROST","TJX","DG","DLTR",
    "KR","ULTA","EL","LULU","DECK","PVH","RL","UAA","PLNT","TSCO",
    "MAR","HLT","H","RCL","CCL","NCLH","EBAY","CAR","ETSY","PDD",
    "JD","BURL","KMX","AZO","ORLY","GPC","GM","F","STLA","HOG",
    "BYD","CZR","LVS","WYNN","MTCH","TAP","SAM","CELH","ELF",
    "CROX","DKS",

    # Consumer Staples
    "PG","PEP","KO","CL","KMB","CHD","HSY","MDLZ","GIS","K",
    "SJM","TSN","CAG","KHC","CLX","STZ","MKC","PM","MO","BG",
    "ADM","UL","BUD",

    # Real Estate (REITs)
    "AMT","PLD","EQIX","DLR","O","PSA","CCI","SBAC","EXR","ARE",
    "VTR","WELL","MAA","AVB","EQR","UDR","ESS","SPG","FRT","KIM",
    "REG","NTST",

    # Utilities
    "NEE","DUK","SO","D","AEP","ED","XEL","PEG","EIX","AWK",
    "AES","ETR","WEC","SRE","PCG","PPL","NRG",

    # Small / Mid-Cap Tech
    "AFRM","COUR","DOCS","TWST","TASK","VERX","APPN","ESTC","FROG",
    "SPSC","OKTA","AI","UPST","FOUR","ENVX","CHWY","GLBE","LCID",
    "RIVN","BILL",

    # Small / Mid-Cap Energy
    "AR","RRC","MTDR","SM","MGY","DINO","VET","CVEO","TALO",
    "CHRD","CIVI","CRC","REI","HPK",

    # Mining / Materials / Clean Energy
    "LTHM","PLL","LAC","SGML","MP","URA","URNM","SMR","CCJ",
    "SCCO","TECK","NEM",

    # Small / Mid-Cap Financials
    "CMA","KEY","RF","HBAN","FITB","CFG","BK","STT","NTRS","BEN",
    "TROW","AMP","RJF","MKTX","MCO","MSCI","SOFI",

    # Retail / Consumer Growth
    "ONON","BIRK","FIGS","SG","BROS","FIVE","WSM","YETI",
    "DKNG","PENN",

    # Defense / Aerospace
    "HII","BWXT","CW","TDG","ACHR","JOBY",

    # ETFs (useful for sector benchmarking)
    "SPY","QQQ","IWM","DIA","VTI","VOO","ARKK","ARKW","SOXX","SMH",
    "XLK","XLF","XLE","XLI","XLV","XLY","XLP","XLU","XLB","XME",
    "XOP","KRE","IYT","IYR","XLRE","XBI","IBB","PBW","TAN","URA",
    "CIBR","HACK","VGT","VDE","VNQ","VOX",
]

OWNED = ["AMD", "HOOD", "MP", "UNH", "SOFI", "OPEN"]

# Rename tickers that have changed since this list was built
ALIASES = {
    "BLL": "BALL",   # Ball Corp → BALL
    "WRK": "SW",     # WestRock  → Smurfit WestRock (SW)
}

# Tickers known to be delisted or invalid — skip silently
SKIP_TICKERS = {"PNRA", "CLR", "SQSP", "ANSS", "GEV", "XYZ"}


def sanitize_tickers(tickers: list) -> tuple:
    """
    Clean a list of tickers:
      - Strip whitespace and uppercase
      - Apply known aliases (e.g. BLL → BALL)
      - Drop known-bad/delisted symbols
      - Remove duplicates while preserving order

    Returns (clean_list, remapped_dict, dropped_list).
    """
    cleaned, remapped, dropped = [], {}, []

    for t in tickers:
        s = t.strip().upper()
        if s in SKIP_TICKERS:
            dropped.append(s)
            continue
        if s in ALIASES:
            remapped[s] = ALIASES[s]
            cleaned.append(ALIASES[s])
        else:
            cleaned.append(s)

    # Remove duplicates while keeping the first occurrence
    clean_unique = list(dict.fromkeys(cleaned))
    return clean_unique, remapped, dropped