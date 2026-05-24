"""Live market data from Binance (no API key required)."""

from __future__ import annotations

import pandas as pd
import requests
from typing import Optional

BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr"
BINANCE_KLINES = "https://api.binance.com/api/v3/klines"

WATCHLIST = [
    ("BTC", "BTCUSDT"),
    ("ETH", "ETHUSDT"),
    ("BNB", "BNBUSDT"),
    ("SOL", "SOLUSDT"),
    ("XRP", "XRPUSDT"),
    ("ADA", "ADAUSDT"),
    ("DOGE", "DOGEUSDT"),
    ("DOT", "DOTUSDT"),
    ("MATIC", "MATICUSDT"),
    ("AVAX", "AVAXUSDT"),
]

CRYPTO_OPTIONS = {
    "Bitcoin (BTC)": "BTCUSDT",
    "Ethereum (ETH)": "ETHUSDT",
    "BNB": "BNBUSDT",
    "Solana (SOL)": "SOLUSDT",
    "XRP": "XRPUSDT",
    "Cardano (ADA)": "ADAUSDT",
    "Dogecoin (DOGE)": "DOGEUSDT",
    "Polkadot (DOT)": "DOTUSDT",
    "Polygon (MATIC)": "MATICUSDT",
    "Avalanche (AVAX)": "AVAXUSDT",
}


def fetch_ticker_24h() -> pd.DataFrame:
    """All 24h tickers from Binance."""
    resp = requests.get(BINANCE_TICKER, timeout=10)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def get_symbol_row(df: pd.DataFrame, symbol: str) -> Optional[pd.Series]:
    rows = df[df["symbol"] == symbol]
    if rows.empty:
        return None
    return rows.iloc[0]


def format_price(price: float) -> str:
    if price >= 1000:
        return f"${price:,.2f}"
    if price >= 1:
        return f"${price:,.4f}"
    return f"${price:.6f}"


def fetch_klines(symbol: str, interval: str = "1h", limit: int = 168) -> pd.DataFrame:
    """OHLCV candles for charting (default ~7 days hourly)."""
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(BINANCE_KLINES, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = df[col].astype(float)
    return df


def top_movers(df: pd.DataFrame, quote: str = "USDT", n: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Top gainers and losers among USDT pairs."""
    usdt = df[df["symbol"].str.endswith(quote)].copy()
    usdt["priceChangePercent"] = usdt["priceChangePercent"].astype(float)
    usdt["lastPrice"] = usdt["lastPrice"].astype(float)
    usdt["quoteVolume"] = usdt["quoteVolume"].astype(float)
    # Filter liquid pairs only
    usdt = usdt[usdt["quoteVolume"] > 1_000_000]
    gainers = usdt.nlargest(n, "priceChangePercent")[
        ["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]
    ]
    losers = usdt.nsmallest(n, "priceChangePercent")[
        ["symbol", "lastPrice", "priceChangePercent", "quoteVolume"]
    ]
    return gainers, losers


def watchlist_snapshot(df: pd.DataFrame) -> list[dict]:
    """Compact watchlist for hub ticker."""
    out = []
    for label, symbol in WATCHLIST:
        row = get_symbol_row(df, symbol)
        if row is None:
            continue
        pct = float(row["priceChangePercent"])
        out.append(
            {
                "label": label,
                "symbol": symbol,
                "price": float(row["lastPrice"]),
                "change_pct": pct,
                "volume": float(row["quoteVolume"]),
            }
        )
    return out
