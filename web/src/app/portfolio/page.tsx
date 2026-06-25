"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { AllocationPie } from "@/components/AllocationPie";
import { HealthGauge } from "@/components/HealthGauge";
import { LoadingState } from "@/components/LoadingState";
import { useProfile } from "@/context/ProfileContext";
import { computeHealthScore } from "@/lib/health-score";
import { computeMarketMood } from "@/lib/market-mood";
import { buildHtmlReport, downloadHtmlReport } from "@/lib/report";
import { generateAdvisorInsights } from "@/lib/insights";
import { currentWealth, formatINR } from "@/lib/format";
import type { CryptoTicker } from "@/lib/types";

export default function PortfolioPage() {
  const { profile, goalsGapTotal } = useProfile();
  const [tickers, setTickers] = useState<CryptoTicker[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/crypto/ticker")
      .then((r) => r.json())
      .then(setTickers)
      .finally(() => setLoading(false));
  }, []);

  const total = currentWealth(profile);
  const cryptoInr = profile.profile_crypto_usd * profile.profile_usd_inr;
  const mfPct = total > 0 ? (profile.profile_mf_value / total) * 100 : 0;
  const cryptoPct = total > 0 ? (cryptoInr / total) * 100 : 0;

  const health = useMemo(
    () =>
      computeHealthScore({
        age: profile.profile_age,
        monthly_income: profile.profile_income,
        monthly_investment: profile.profile_sip,
        has_emergency_fund: profile.profile_emergency_fund,
        has_insurance: profile.profile_insurance,
        equity_pct: profile.profile_equity,
      }),
    [profile]
  );

  const mood = useMemo(() => computeMarketMood(tickers), [tickers]);

  const pieData = [
    { name: "Mutual Funds", value: profile.profile_mf_value },
    { name: "Crypto", value: cryptoInr },
  ].filter((d) => d.value > 0);

  const exportReport = useCallback(() => {
    const insights = generateAdvisorInsights(profile, mood.score, mood.label, goalsGapTotal);
    const html = buildHtmlReport({
      profile,
      health_score: health.score,
      health_grade: health.grade,
      insights: insights.map((i) => i.title),
      total_portfolio: total,
      mood_label: mood.label,
      mood_score: mood.score,
    });
    downloadHtmlReport(html);
  }, [profile, mood, goalsGapTotal, health, total]);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">💓 Portfolio Pulse</h1>
          <p className="mt-1 text-slate-400">Unified asset mix · health score · exportable report</p>
        </div>
        <button type="button" onClick={exportReport} className="btn-primary">
          📄 Download HTML report
        </button>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="stat-box">
          <div className="num">{formatINR(total)}</div>
          <div className="lbl">Total portfolio</div>
        </div>
        <div className="stat-box">
          <div className="num">{mfPct.toFixed(0)}%</div>
          <div className="lbl">MF weight</div>
        </div>
        <div className="stat-box">
          <div className="num">{cryptoPct.toFixed(0)}%</div>
          <div className="lbl">Crypto weight</div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card flex flex-col items-center">
          <h2 className="mb-4 self-start font-semibold">Financial health</h2>
          <HealthGauge score={health.score} grade={health.grade} color={health.color} />
          <div className="mt-6 w-full space-y-2">
            {Object.entries(health.breakdown).map(([k, v]) => (
              <div key={k} className="flex justify-between text-sm">
                <span className="text-slate-400">{k}</span>
                <span className="font-mono">{v}/20</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card">
          <h2 className="mb-3 font-semibold">Asset mix</h2>
          {pieData.length > 0 ? (
            <AllocationPie data={pieData} />
          ) : (
            <p className="text-sm text-slate-400">Add holdings in your profile</p>
          )}
        </div>
      </div>

      <div className="glass-card">
        <h2 className="mb-2 font-semibold">Health insights</h2>
        <ul className="list-inside list-disc space-y-1 text-sm text-slate-300">
          {health.insights.map((ins, i) => (
            <li key={i}>{ins}</li>
          ))}
        </ul>
      </div>

      {loading ? (
        <LoadingState label="Loading market mood…" />
      ) : (
        <div className="glass-card text-sm">
          <p>
            Crypto mood: <span style={{ color: mood.color }}>{mood.label}</span> ({mood.score}/100)
          </p>
        </div>
      )}
    </div>
  );
}
