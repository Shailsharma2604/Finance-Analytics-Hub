"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { MonteCarloChart } from "@/components/MonteCarloChart";
import { LoadingState } from "@/components/LoadingState";
import { ErrorAlert } from "@/components/ErrorAlert";
import { useProfile } from "@/context/ProfileContext";
import { runMonteCarlo } from "@/lib/simulator";
import { computeMarketMood } from "@/lib/market-mood";
import { formatINRDecimal, formatPct, currentWealth } from "@/lib/format";
import type { CryptoTicker, IndiaIndex } from "@/lib/types";
import { WATCHLIST } from "@/lib/constants";

export default function CommandCenterPage() {
  const { profile } = useProfile();
  const [indices, setIndices] = useState<IndiaIndex[]>([]);
  const [tickers, setTickers] = useState<CryptoTicker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [sip, setSip] = useState(profile.profile_sip);
  const [years, setYears] = useState(profile.profile_target_years);
  const [lumpSum, setLumpSum] = useState(currentWealth(profile));

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [idxRes, tickRes] = await Promise.all([
        fetch("/api/india/indices"),
        fetch("/api/crypto/ticker"),
      ]);
      if (!idxRes.ok) throw new Error("India indices unavailable");
      if (!tickRes.ok) throw new Error("Crypto ticker unavailable");
      const idxJson = await idxRes.json();
      const tickJson = await tickRes.json();
      setIndices(idxJson.indices ?? []);
      setTickers(tickJson);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load markets");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const mood = useMemo(() => computeMarketMood(tickers), [tickers]);

  const watchlist = useMemo(() => {
    return WATCHLIST.map(([label, symbol]) => {
      const row = tickers.find((t) => t.symbol === symbol);
      if (!row) return null;
      return {
        label,
        price: parseFloat(row.lastPrice),
        change: parseFloat(row.priceChangePercent),
      };
    }).filter(Boolean) as { label: string; price: number; change: number }[];
  }, [tickers]);

  const mc = useMemo(
    () =>
      runMonteCarlo(
        sip,
        lumpSum,
        years,
        profile.profile_expected_return / 100,
        0.18
      ),
    [sip, lumpSum, years, profile.profile_expected_return]
  );

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">🏠 Command Center</h1>
        <p className="mt-1 text-slate-400">India indices · crypto mood · Monte Carlo</p>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorAlert message={error} onRetry={fetchData} />}

      {!loading && !error && (
        <>
          <section>
            <h2 className="mb-3 font-semibold">🇮🇳 India Indices</h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {indices.map((idx) => (
                <div key={idx.name} className="glass-card">
                  <p className="text-sm text-slate-400">{idx.name}</p>
                  <p className="font-mono text-xl font-bold">{formatINRDecimal(idx.price)}</p>
                  <p className={idx.change_pct >= 0 ? "text-accent" : "text-rose-400"}>
                    {formatPct(idx.change_pct)}
                  </p>
                </div>
              ))}
            </div>
          </section>

          <section className="grid gap-6 lg:grid-cols-2">
            <div className="glass-card">
              <h2 className="mb-3 font-semibold">₿ Crypto Mood Index</h2>
              <div className="flex items-center gap-6">
                <div
                  className="font-mono text-5xl font-bold"
                  style={{ color: mood.color }}
                >
                  {mood.score}
                </div>
                <div>
                  <p className="text-lg font-semibold" style={{ color: mood.color }}>
                    {mood.label}
                  </p>
                  <p className="text-sm text-slate-400">
                    Rising pairs: {mood.details.pairs_rising} · BTC: {mood.details.btc_24h}
                  </p>
                </div>
              </div>
            </div>

            <div className="glass-card">
              <h2 className="mb-3 font-semibold">Watchlist</h2>
              <div className="space-y-2">
                {watchlist.map((w) => (
                  <div key={w.label} className="flex justify-between text-sm">
                    <span>{w.label}</span>
                    <span>
                      ${w.price.toLocaleString()}{" "}
                      <span className={w.change >= 0 ? "text-accent" : "text-rose-400"}>
                        {formatPct(w.change)}
                      </span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="glass-card">
            <h2 className="mb-4 font-semibold">📊 Monte Carlo Wealth Simulator</h2>
            <div className="mb-4 grid gap-4 sm:grid-cols-3">
              <label className="text-sm">
                Monthly SIP (₹)
                <input
                  type="number"
                  className="input-field mt-1"
                  value={sip}
                  onChange={(e) => setSip(Number(e.target.value))}
                />
              </label>
              <label className="text-sm">
                Lump sum (₹)
                <input
                  type="number"
                  className="input-field mt-1"
                  value={lumpSum}
                  onChange={(e) => setLumpSum(Number(e.target.value))}
                />
              </label>
              <label className="text-sm">
                Years
                <input
                  type="number"
                  className="input-field mt-1"
                  value={years}
                  min={1}
                  max={40}
                  onChange={(e) => setYears(Number(e.target.value))}
                />
              </label>
            </div>
            <MonteCarloChart data={mc} />
            <div className="mt-4 grid grid-cols-3 gap-3 text-center text-sm">
              <div>
                <p className="text-slate-400">Median corpus</p>
                <p className="font-mono font-bold text-accent">
                  ₹{mc.final_median.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
                </p>
              </div>
              <div>
                <p className="text-slate-400">P10 (bear)</p>
                <p className="font-mono">₹{mc.final_p10.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</p>
              </div>
              <div>
                <p className="text-slate-400">P90 (bull)</p>
                <p className="font-mono">₹{mc.final_p90.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</p>
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
