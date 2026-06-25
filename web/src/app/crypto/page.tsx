"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { CryptoPriceChart } from "@/components/CryptoPriceChart";
import { LoadingState } from "@/components/LoadingState";
import { ErrorAlert } from "@/components/ErrorAlert";
import { useProfile } from "@/context/ProfileContext";
import { topMovers } from "@/lib/market-mood";
import { formatPct, formatUSD } from "@/lib/format";
import { CRYPTO_OPTIONS } from "@/lib/constants";
import { fallbackBannerMessage, parseTickerResponse, type CryptoDataSource } from "@/lib/crypto-fetch";
import type { CryptoTicker } from "@/lib/types";

interface Candle {
  time: string;
  close: number;
}

export default function CryptoPage() {
  const { paperPortfolio, setPaperQty } = useProfile();
  const [tickers, setTickers] = useState<CryptoTicker[]>([]);
  const [candles, setCandles] = useState<Candle[]>([]);
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [loading, setLoading] = useState(true);
  const [chartLoading, setChartLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<CryptoDataSource>("binance");
  const [buyQty, setBuyQty] = useState(0.01);

  const fetchTicker = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/crypto/ticker");
      if (!res.ok) throw new Error("Crypto data unavailable");
      const parsed = parseTickerResponse(await res.json());
      setTickers(parsed.tickers);
      setDataSource(parsed.source);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchChart = useCallback(async (sym: string) => {
    setChartLoading(true);
    try {
      const res = await fetch(`/api/crypto/klines?symbol=${sym}&interval=1h&limit=168`);
      if (!res.ok) throw new Error("Chart data unavailable");
      const json = await res.json();
      setCandles(json.candles ?? []);
    } catch {
      setCandles([]);
    } finally {
      setChartLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTicker();
  }, [fetchTicker]);

  useEffect(() => {
    fetchChart(symbol);
  }, [symbol, fetchChart]);

  const { gainers, losers } = useMemo(() => topMovers(tickers), [tickers]);

  const paperValue = useMemo(() => {
    let total = 0;
    for (const [sym, qty] of Object.entries(paperPortfolio)) {
      const row = tickers.find((t) => t.symbol === sym);
      if (row) total += parseFloat(row.lastPrice) * qty;
    }
    return total;
  }, [paperPortfolio, tickers]);

  const addPaper = () => {
    const current = paperPortfolio[symbol] ?? 0;
    setPaperQty(symbol, current + buyQty);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">₿ Crypto Intelligence</h1>
        <p className="mt-1 text-slate-400">Charts · top movers · paper portfolio</p>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorAlert message={error} onRetry={fetchTicker} />}

      {!loading && !error && (
        <>
          {fallbackBannerMessage(dataSource) && (
            <p className="rounded-lg border border-sky-500/30 bg-sky-500/10 px-4 py-2 text-sm text-sky-200">
              {fallbackBannerMessage(dataSource)}
            </p>
          )}
          <div className="glass-card">
            <label className="text-sm">
              Chart symbol
              <select
                className="input-field mt-1"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
              >
                {Object.entries(CRYPTO_OPTIONS).map(([label, sym]) => (
                  <option key={sym} value={sym}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            {chartLoading ? (
              <LoadingState label="Loading chart…" />
            ) : candles.length > 0 ? (
              <CryptoPriceChart candles={candles} symbol={symbol} />
            ) : (
              <p className="mt-4 text-sm text-slate-400">No chart data</p>
            )}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="glass-card">
              <h2 className="mb-3 font-semibold text-accent">🚀 Top gainers (24h)</h2>
              <div className="space-y-2 text-sm">
                {gainers.map((g) => (
                  <div key={g.symbol} className="flex justify-between">
                    <span>{g.symbol.replace("USDT", "")}</span>
                    <span>
                      {formatUSD(parseFloat(g.lastPrice))}{" "}
                      <span className="text-accent">{formatPct(parseFloat(g.priceChangePercent))}</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <div className="glass-card">
              <h2 className="mb-3 font-semibold text-rose-400">📉 Top losers (24h)</h2>
              <div className="space-y-2 text-sm">
                {losers.map((g) => (
                  <div key={g.symbol} className="flex justify-between">
                    <span>{g.symbol.replace("USDT", "")}</span>
                    <span>
                      {formatUSD(parseFloat(g.lastPrice))}{" "}
                      <span className="text-rose-400">{formatPct(parseFloat(g.priceChangePercent))}</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="glass-card">
            <h2 className="mb-3 font-semibold">📝 Paper portfolio</h2>
            <p className="text-sm text-slate-400">Simulated holdings — no real trades</p>
            <div className="mt-4 flex flex-wrap items-end gap-3">
              <label className="text-sm">
                Qty to add
                <input
                  type="number"
                  step="0.001"
                  className="input-field mt-1 w-32"
                  value={buyQty}
                  onChange={(e) => setBuyQty(Number(e.target.value))}
                />
              </label>
              <button type="button" onClick={addPaper} className="btn-primary">
                Add {symbol.replace("USDT", "")}
              </button>
            </div>
            <p className="mt-4 font-mono text-lg text-accent">
              Paper value: {formatUSD(paperValue)}
            </p>
            <div className="mt-3 space-y-1 text-sm">
              {Object.entries(paperPortfolio).map(([sym, qty]) => {
                const price = tickers.find((t) => t.symbol === sym);
                const val = price ? parseFloat(price.lastPrice) * qty : 0;
                return (
                  <div key={sym} className="flex justify-between">
                    <span>
                      {sym.replace("USDT", "")} × {qty}
                    </span>
                    <span>
                      {formatUSD(val)}{" "}
                      <button
                        type="button"
                        className="text-rose-400 underline"
                        onClick={() => setPaperQty(sym, 0)}
                      >
                        clear
                      </button>
                    </span>
                  </div>
                );
              })}
              {Object.keys(paperPortfolio).length === 0 && (
                <p className="text-slate-500">No paper holdings yet</p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
