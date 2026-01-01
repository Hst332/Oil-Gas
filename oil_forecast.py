#!/usr/bin/env python3
"""
CODE A – Oil Forecast
Brent + WTI + Spread
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

START_DATE = "2015-01-01"
SYMBOL_BRENT = "BZ=F"
SYMBOL_WTI = "CL=F"


def run_oil_forecast():
    brent = yf.download(SYMBOL_BRENT, start=START_DATE, progress=False)
    wti = yf.download(SYMBOL_WTI, start=START_DATE, progress=False)

    df = pd.DataFrame(index=brent.index)
    df["Brent"] = brent["Close"]
    df["WTI"] = wti["Close"]
    df.dropna(inplace=True)

    df["Brent_Trend"] = df["Brent"] > df["Brent"].rolling(20).mean()
    df["WTI_Trend"] = df["WTI"] > df["WTI"].rolling(20).mean()

    df["Spread"] = df["Brent"] - df["WTI"]
    df["Spread_Z"] = (
        (df["Spread"] - df["Spread"].rolling(60).mean())
        / df["Spread"].rolling(60).std()
    )

    df.dropna(inplace=True)
    last = df.iloc[-1]

    prob_up = 0.50
    if last["Brent_Trend"] and last["WTI_Trend"]:
        prob_up += 0.07
    if last["Spread_Z"] > 0.5:
        prob_up += 0.03
    elif last["Spread_Z"] < -0.5:
        prob_up -= 0.03

    prob_up = max(0.0, min(1.0, prob_up))

    if prob_up >= 0.57:
        signal = "UP"
    elif prob_up <= 0.43:
        signal = "DOWN"
    else:
        signal = "NO_TRADE"

    return {
        "section": "OIL",
        "run_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "data_date": last.name.date().isoformat(),
        "prob_up": prob_up,
        "prob_down": 1 - prob_up,
        "signal": signal,
        "brent": float(last["Brent"]),
        "wti": float(last["WTI"]),
        "spread": float(last["Spread"]),
    }
