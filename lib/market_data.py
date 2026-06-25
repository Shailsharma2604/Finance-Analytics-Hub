"""Live market data with Binance primary and CoinGecko fallback (no API key)."""

from __future__ import annotations

import pandas as pd
import requests
from typing import Literal, Optional

BINANCE_BASES = (
    "https://api.binance.com/api/v3",
    "https://api.binance.us/api/v3",
)
COINGECKO_MARKETS = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_OHLC = "https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"

DataSource = Literal["binance", "binance.us", "coingecko"]

# Binance USDT symbol → CoinGecko coin id
SYMBOL_TO_COINGECKO_ID: dict[str, str] = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binancecoin",
    "SOLUSDT": "solana",
    "XRPUSDT": "ripple",
    "ADAUSDT": "cardano",
    "DOGEUSDT": "dogecoin",
    "DOTUSDT": "polkadot",
    "MATICUSDT": "polygon-ecosystem-token",
    "AVAXUSDT": "avalanche-2",
}

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


def data_source_banner(source: DataSource) -> Optional[str]:
    """User-facing notice when not on primary Binance.com feed."""
    if source == "coingecko":
        return "Using CoinGecko (Binance unavailable in this region)"
    if source == "binance.us":
        return "Using Binance US (Binance.com unavailable in this region)"
    return None


def _binance_source(base: str) -> DataSource:
    return "binance" if "binance.com" in base else "binance.us"


def _try_binance_get(url: str) -> Optional[requests.Response]:
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code in (451, 403):
            return None
        resp.raise_for_status()
        return resp
    except requests.RequestException:
        return None


def _coingecko_rows_from_markets(coins: list) -> list[dict]:
    rows = []
    id_to_symbol = {v: k for k, v in SYMBOL_TO_COINGECKO_ID.items()}
    for coin in coins:
        coin_id = coin.get("id", "")
        sym = str(coin.get("symbol", "")).upper()
        if not sym and coin_id not in id_to_symbol:
            continue
        price = coin.get("current_price")
        if price is None:
            continue
        pct = coin.get("price_change_percentage_24h") or 0.0
        vol = coin.get("total_volume") or 0.0
        high = coin.get("high_24h") or price
        low = coin.get("low_24h") or price
        symbol = id_to_symbol.get(coin_id, f"{sym}USDT")
        rows.append(
            {
                "symbol": symbol,
                "lastPrice": str(price),
                "priceChangePercent": str(pct),
                "quoteVolume": str(vol),
                "highPrice": str(high),
                "lowPrice": str(low),
            }
        )
    return rows


def _fetch_coingecko_ticker() -> pd.DataFrame:
    resp = requests.get(
        COINGECKO_MARKETS,
        params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h",
        },
        timeout=15,
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    rows = _coingecko_rows_from_markets(resp.json())
    found = {r["symbol"] for r in rows}
    missing_ids = [
        cg_id for sym, cg_id in SYMBOL_TO_COINGECKO_ID.items() if sym not in found
    ]
    if missing_ids:
        extra = requests.get(
            COINGECKO_MARKETS,
            params={
                "vs_currency": "usd",
                "ids": ",".join(missing_ids),
                "sparkline": "false",
                "price_change_percentage": "24h",
            },
            timeout=15,
            headers={"Accept": "application/json"},
        )
        extra.raise_for_status()
        rows.extend(_coingecko_rows_from_markets(extra.json()))
    if not rows:
        raise RuntimeError("CoinGecko returned no market data")
    return pd.DataFrame(rows)


def fetch_ticker_24h_with_source() -> tuple[pd.DataFrame, DataSource]:
    """24h tickers — Binance.com → Binance US → CoinGecko."""
    for base in BINANCE_BASES:
        resp = _try_binance_get(f"{base}/ticker/24hr")
        if resp is not None:
            return pd.DataFrame(resp.json()), _binance_source(base)
    return _fetch_coingecko_ticker(), "coingecko"


def fetch_ticker_24h() -> pd.DataFrame:
    """All 24h tickers (backward-compatible wrapper)."""
    df, _ = fetch_ticker_24h_with_source()
    return df


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


def _coingecko_days(interval: str, limit: int) -> int:
    if interval == "1d":
        return min(90, max(30, limit))
    if interval == "4h":
        return min(30, max(7, (limit * 4) // 24 + 1))
    return min(30, max(1, limit // 24 + 1))


def _fetch_coingecko_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    coin_id = SYMBOL_TO_COINGECKO_ID.get(symbol)
    if not coin_id:
        raise ValueError(f"No CoinGecko mapping for {symbol}")
    days = _coingecko_days(interval, limit)
    url = COINGECKO_OHLC.format(coin_id=coin_id)
    resp = requests.get(
        url,
        params={"vs_currency": "usd", "days": days},
        timeout=15,
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise RuntimeError(f"CoinGecko OHLC empty for {symbol}")
    trimmed = data[-limit:] if len(data) > limit else data
    df = pd.DataFrame(trimmed, columns=["open_time", "open", "high", "low", "close"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ("open", "high", "low", "close"):
        df[col] = df[col].astype(float)
    df["volume"] = 0.0
    return df


def fetch_klines_with_source(
    symbol: str, interval: str = "1h", limit: int = 168
) -> tuple[pd.DataFrame, DataSource]:
    """OHLCV candles — Binance.com → Binance US → CoinGecko."""
    params = f"symbol={symbol}&interval={interval}&limit={limit}"
    for base in BINANCE_BASES:
        resp = _try_binance_get(f"{base}/klines?{params}")
        if resp is not None:
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
            return df, _binance_source(base)
    return _fetch_coingecko_klines(symbol, interval, limit), "coingecko"


def fetch_klines(symbol: str, interval: str = "1h", limit: int = 168) -> pd.DataFrame:
    """OHLCV candles for charting (default ~7 days hourly)."""
    df, _ = fetch_klines_with_source(symbol, interval=interval, limit=limit)
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
