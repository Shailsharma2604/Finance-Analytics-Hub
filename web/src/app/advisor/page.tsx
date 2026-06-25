"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { LoadingState } from "@/components/LoadingState";
import { ErrorAlert } from "@/components/ErrorAlert";
import { useProfile } from "@/context/ProfileContext";
import { generateAdvisorInsights } from "@/lib/insights";
import { computeMarketMood } from "@/lib/market-mood";
import { buildHtmlReport, downloadHtmlReport } from "@/lib/report";
import { computeHealthScore } from "@/lib/health-score";
import { currentWealth } from "@/lib/format";
import type { CryptoTicker } from "@/lib/types";

export default function AdvisorPage() {
  const { profile, goalsGapTotal } = useProfile();
  const [tickers, setTickers] = useState<CryptoTicker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/crypto/ticker");
      if (!res.ok) throw new Error("Market data unavailable");
      setTickers(await res.json());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const mood = useMemo(() => computeMarketMood(tickers), [tickers]);
  const insights = useMemo(
    () => generateAdvisorInsights(profile, mood.score, mood.label, goalsGapTotal),
    [profile, mood, goalsGapTotal]
  );

  const exportReport = () => {
    const health = computeHealthScore({
      age: profile.profile_age,
      monthly_income: profile.profile_income,
      monthly_investment: profile.profile_sip,
      has_emergency_fund: profile.profile_emergency_fund,
      has_insurance: profile.profile_insurance,
      equity_pct: profile.profile_equity,
    });
    const html = buildHtmlReport({
      profile,
      health_score: health.score,
      health_grade: health.grade,
      insights: insights.map((i) => `${i.title}: ${i.body}`),
      total_portfolio: currentWealth(profile),
      mood_label: mood.label,
      mood_score: mood.score,
    });
    downloadHtmlReport(html);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">🧠 AI Advisor</h1>
          <p className="mt-1 text-slate-400">Rule-based prioritized insights from profile + markets</p>
        </div>
        <button type="button" onClick={exportReport} className="btn-primary">
          📄 Export HTML report
        </button>
      </div>

      {loading && <LoadingState label="Loading market context…" />}
      {error && <ErrorAlert message={error} onRetry={fetchData} />}

      {!loading && (
        <div className="space-y-4">
          {insights.map((ins, i) => (
            <div
              key={i}
              className="glass-card border-l-4"
              style={{ borderLeftColor: i === 0 ? "#00d4aa" : "rgba(255,255,255,0.2)" }}
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-full bg-white/10 px-2 py-0.5 text-xs">{ins.category}</span>
                <h3 className="font-semibold">{ins.title}</h3>
              </div>
              <p className="mt-2 text-sm text-slate-300">{ins.body}</p>
              <p className="mt-2 text-sm text-accent">→ {ins.action}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
