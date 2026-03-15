import numpy as np


def detect_volatility_regime(data, window=20):

    returns = data["Close"].pct_change()

    vol = returns.rolling(window).std()

    current_vol = vol.iloc[-1]

    avg_vol = vol.mean()

    if current_vol > avg_vol * 1.5:
        return "HIGH_VOL"

    elif current_vol < avg_vol * 0.7:
        return "LOW_VOL"

    else:
        return "NORMAL_VOL"
