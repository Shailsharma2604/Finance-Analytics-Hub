"""Crypto market mood index (0–100) from live ticker data."""

from __future__ import annotations

import pandas as pd


def compute_market_mood(df: pd.DataFrame) -> dict:
    """
    Derive a fear/greed style score from USDT pair stats.
    0 = extreme fear, 100 = extreme greed.
    """
    usdt = df[df["symbol"].str.endswith("USDT")].copy()
    if usdt.empty:
        return {"score": 50, "label": "Neutral", "color": "#fbbf24", "details": {}}

    usdt["priceChangePercent"] = usdt["priceChangePercent"].astype(float)
    usdt["quoteVolume"] = usdt["quoteVolume"].astype(float)
    liquid = usdt[usdt["quoteVolume"] > 500_000]

    pct_positive = (liquid["priceChangePercent"] > 0).mean() * 100
    avg_change = liquid["priceChangePercent"].mean()
    avg_change = max(-15, min(15, avg_change))
    avg_norm = (avg_change + 15) / 30 * 100

    btc_row = usdt[usdt["symbol"] == "BTCUSDT"]
    btc_change = float(btc_row["priceChangePercent"].iloc[0]) if len(btc_row) else 0
    btc_norm = (max(-10, min(10, btc_change)) + 10) / 20 * 100

    vol_median = liquid["quoteVolume"].median()
    high_vol = (liquid["quoteVolume"] > vol_median * 2).sum()
    vol_stress = max(0, 100 - high_vol / max(len(liquid), 1) * 200)

    score = 0.35 * pct_positive + 0.30 * avg_norm + 0.25 * btc_norm + 0.10 * vol_stress
    score = int(max(0, min(100, score)))

    if score >= 75:
        label, color = "Extreme Greed", "#00d4aa"
    elif score >= 55:
        label, color = "Greed", "#34d399"
    elif score >= 45:
        label, color = "Neutral", "#fbbf24"
    elif score >= 25:
        label, color = "Fear", "#fb923c"
    else:
        label, color = "Extreme Fear", "#f43f5e"

    return {
        "score": score,
        "label": label,
        "color": color,
        "details": {
            "pairs_rising": f"{pct_positive:.0f}%",
            "avg_change": f"{avg_change:+.2f}%",
            "btc_24h": f"{btc_change:+.2f}%",
        },
    }
