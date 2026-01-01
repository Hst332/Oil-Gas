#!/usr/bin/env python3
"""
CODE A – Natural Gas Forecast
Stabil. Getestet. Serien-sicher.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score

START_DATE = "2014-01-01"
GAS_SYMBOL = "NG=F"

UP_THRESHOLD = 0.60
DOWN_THRESHOLD = 0.40


def run_gas_forecast():
    df = yf.download(GAS_SYMBOL, start=START_DATE, auto_adjust=True, progress=False)
    df = df[["Close"]].rename(columns={"Close": "Gas_Close"})
    df.dropna(inplace=True)

    df["ret"] = df["Gas_Close"].pct_change()
    df["trend_5"] = df["Gas_Close"].pct_change(5)
    df["trend_20"] = df["Gas_Close"].pct_change(20)
    df["vol_10"] = df["ret"].rolling(10).std()

    df["Target"] = (df["ret"].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)

    features = ["trend_5", "trend_20", "vol_10"]
    X = df[features]
    y = df["Target"]

    tscv = TimeSeriesSplit(5)
    acc = []

    for tr, te in tscv.split(X):
        m = LogisticRegression(max_iter=200)
        m.fit(X.iloc[tr], y.iloc[tr])
        acc.append(accuracy_score(y.iloc[te], m.predict(X.iloc[te])))

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    last = X.iloc[[-1]]  # <<< WICHTIG: DataFrame, kein Series
    prob_up = model.predict_proba(last)[0][1]

    if prob_up >= UP_THRESHOLD:
        signal = "UP"
    elif prob_up <= DOWN_THRESHOLD:
        signal = "DOWN"
    else:
        signal = "NO_TRADE"

    return {
        "section": "NATURAL GAS",
        "run_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "data_date": df.index[-1].date().isoformat(),
        "prob_up": prob_up,
        "prob_down": 1 - prob_up,
        "signal": signal,
        "cv_mean": float(np.mean(acc)),
        "cv_std": float(np.std(acc)),
    }
