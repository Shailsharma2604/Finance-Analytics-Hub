"""Indian equity indices via Yahoo Finance chart API (no key)."""

from __future__ import annotations

import requests

INDICES = {
    "Nifty 50": "%5ENSEI",
    "Sensex": "%5EBSESN",
    "Bank Nifty": "%5ENSEBANK",
    "Nifty IT": "%5ENSEIT",
}


def _fetch_chart(symbol_encoded: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol_encoded}"
    params = {"interval": "1d", "range": "5d"}
    try:
        r = requests.get(url, params=params, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        result = r.json()["chart"]["result"][0]
        meta = result["meta"]
        closes = result["indicators"]["quote"][0]["close"]
        closes = [c for c in closes if c is not None]
        prev = closes[-2] if len(closes) >= 2 else meta.get("chartPreviousClose", meta["regularMarketPrice"])
        price = meta["regularMarketPrice"]
        chg = ((price - prev) / prev * 100) if prev else 0
        return {
            "price": price,
            "change_pct": chg,
            "currency": meta.get("currency", "INR"),
            "sparkline": closes[-5:],
        }
    except Exception:
        return None


def fetch_india_indices() -> list[dict]:
    out = []
    for name, sym in INDICES.items():
        data = _fetch_chart(sym)
        if data:
            out.append({"name": name, **data})
    return out


def format_inr(price: float) -> str:
    if price >= 1000:
        return f"₹{price:,.2f}"
    return f"₹{price:.2f}"
