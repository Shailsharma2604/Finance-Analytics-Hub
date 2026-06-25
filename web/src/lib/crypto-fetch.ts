import type { CryptoTicker } from "./types";

export type CryptoDataSource = "binance" | "binance.us" | "coingecko";

const BINANCE_BASES = [
  "https://api.binance.com/api/v3",
  "https://api.binance.us/api/v3",
] as const;

const COINGECKO_MARKETS = "https://api.coingecko.com/api/v3/coins/markets";
const COINGECKO_OHLC = "https://api.coingecko.com/api/v3/coins";

const SYMBOL_TO_COINGECKO_ID: Record<string, string> = {
  BTCUSDT: "bitcoin",
  ETHUSDT: "ethereum",
  BNBUSDT: "binancecoin",
  SOLUSDT: "solana",
  XRPUSDT: "ripple",
  ADAUSDT: "cardano",
  DOGEUSDT: "dogecoin",
  DOTUSDT: "polkadot",
  MATICUSDT: "polygon-ecosystem-token",
  AVAXUSDT: "avalanche-2",
};

export function fallbackBannerMessage(source: CryptoDataSource): string | null {
  if (source === "coingecko") {
    return "Using CoinGecko (Binance unavailable in this region)";
  }
  if (source === "binance.us") {
    return "Using Binance US (Binance.com unavailable in this region)";
  }
  return null;
}

function binanceSource(base: string): CryptoDataSource {
  return base.includes("binance.com") ? "binance" : "binance.us";
}

async function tryBinanceFetch(url: string): Promise<Response | null> {
  try {
    const resp = await fetch(url, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (resp.status === 451 || resp.status === 403 || !resp.ok) {
      return null;
    }
    return resp;
  } catch {
    return null;
  }
}

async function fetchCoinGeckoTickers(): Promise<CryptoTicker[]> {
  const url = new URL(COINGECKO_MARKETS);
  url.searchParams.set("vs_currency", "usd");
  url.searchParams.set("order", "market_cap_desc");
  url.searchParams.set("per_page", "250");
  url.searchParams.set("page", "1");
  url.searchParams.set("sparkline", "false");
  url.searchParams.set("price_change_percentage", "24h");

  const resp = await fetch(url.toString(), {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });
  if (!resp.ok) {
    throw new Error(`CoinGecko markets failed: ${resp.status}`);
  }

  const tickers = coingeckoToTickers((await resp.json()) as CoinGeckoMarket[]);
  const found = new Set(tickers.map((t) => t.symbol));
  const missingIds = Object.entries(SYMBOL_TO_COINGECKO_ID)
    .filter(([sym]) => !found.has(sym))
    .map(([, id]) => id);

  if (missingIds.length) {
    const extraUrl = new URL(COINGECKO_MARKETS);
    extraUrl.searchParams.set("vs_currency", "usd");
    extraUrl.searchParams.set("ids", missingIds.join(","));
    extraUrl.searchParams.set("sparkline", "false");
    extraUrl.searchParams.set("price_change_percentage", "24h");
    const extraResp = await fetch(extraUrl.toString(), {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (extraResp.ok) {
      tickers.push(...coingeckoToTickers((await extraResp.json()) as CoinGeckoMarket[]));
    }
  }

  if (!tickers.length) {
    throw new Error("CoinGecko returned no market data");
  }
  return tickers;
}

type CoinGeckoMarket = {
  id?: string;
  symbol?: string;
  current_price?: number;
  price_change_percentage_24h?: number | null;
  total_volume?: number;
};

function coingeckoToTickers(coins: CoinGeckoMarket[]): CryptoTicker[] {
  const idToSymbol = Object.fromEntries(
    Object.entries(SYMBOL_TO_COINGECKO_ID).map(([sym, id]) => [id, sym])
  );
  const tickers: CryptoTicker[] = [];
  for (const coin of coins) {
    const sym = coin.symbol?.toUpperCase();
    const coinId = coin.id;
    if ((!sym && !coinId) || coin.current_price == null) continue;
    const symbol = (coinId && idToSymbol[coinId]) || `${sym}USDT`;
    tickers.push({
      symbol,
      lastPrice: String(coin.current_price),
      priceChangePercent: String(coin.price_change_percentage_24h ?? 0),
      quoteVolume: String(coin.total_volume ?? 0),
    });
  }
  return tickers;
}

export async function fetchCryptoTickers(): Promise<{
  tickers: CryptoTicker[];
  source: CryptoDataSource;
}> {
  for (const base of BINANCE_BASES) {
    const resp = await tryBinanceFetch(`${base}/ticker/24hr`);
    if (resp) {
      const data = (await resp.json()) as CryptoTicker[];
      const usdt = data.filter((t) => t.symbol.endsWith("USDT"));
      return { tickers: usdt, source: binanceSource(base) };
    }
  }
  const tickers = await fetchCoinGeckoTickers();
  return { tickers, source: "coingecko" };
}

function coingeckoDays(interval: string, limit: number): number {
  if (interval === "1d") return Math.min(90, Math.max(30, limit));
  if (interval === "4h") return Math.min(30, Math.max(7, Math.floor((limit * 4) / 24) + 1));
  return Math.min(30, Math.max(1, Math.floor(limit / 24) + 1));
}

async function fetchCoinGeckoKlines(
  symbol: string,
  interval: string,
  limit: number
): Promise<{ time: string; open: number; high: number; low: number; close: number; volume: number }[]> {
  const coinId = SYMBOL_TO_COINGECKO_ID[symbol];
  if (!coinId) {
    throw new Error(`No CoinGecko mapping for ${symbol}`);
  }
  const days = coingeckoDays(interval, limit);
  const url = new URL(`${COINGECKO_OHLC}/${coinId}/ohlc`);
  url.searchParams.set("vs_currency", "usd");
  url.searchParams.set("days", String(days));

  const resp = await fetch(url.toString(), {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });
  if (!resp.ok) {
    throw new Error(`CoinGecko OHLC failed: ${resp.status}`);
  }

  const raw = (await resp.json()) as number[][];
  const trimmed = raw.length > limit ? raw.slice(-limit) : raw;
  return trimmed.map((c) => ({
    time: new Date(c[0]).toISOString(),
    open: c[1],
    high: c[2],
    low: c[3],
    close: c[4],
    volume: 0,
  }));
}

export async function fetchCryptoKlines(
  symbol: string,
  interval: string,
  limit: number
): Promise<{
  symbol: string;
  interval: string;
  candles: { time: string; open: number; high: number; low: number; close: number; volume: number }[];
  source: CryptoDataSource;
}> {
  const params = new URLSearchParams({ symbol, interval, limit: String(limit) });

  for (const base of BINANCE_BASES) {
    const resp = await tryBinanceFetch(`${base}/klines?${params}`);
    if (resp) {
      const raw = (await resp.json()) as (string | number)[][];
      const candles = raw.map((c) => ({
        time: new Date(Number(c[0])).toISOString(),
        open: parseFloat(String(c[1])),
        high: parseFloat(String(c[2])),
        low: parseFloat(String(c[3])),
        close: parseFloat(String(c[4])),
        volume: parseFloat(String(c[5])),
      }));
      return { symbol, interval, candles, source: binanceSource(base) };
    }
  }

  const candles = await fetchCoinGeckoKlines(symbol, interval, limit);
  return { symbol, interval, candles, source: "coingecko" };
}

export function parseTickerResponse(json: unknown): {
  tickers: CryptoTicker[];
  source: CryptoDataSource;
} {
  if (Array.isArray(json)) {
    return { tickers: json as CryptoTicker[], source: "binance" };
  }
  const obj = json as { tickers?: CryptoTicker[]; source?: CryptoDataSource };
  return { tickers: obj.tickers ?? [], source: obj.source ?? "binance" };
}
