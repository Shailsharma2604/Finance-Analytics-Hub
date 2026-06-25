"use client";

import { useMemo } from "react";
import { AllocationPie } from "@/components/AllocationPie";
import { useProfile } from "@/context/ProfileContext";
import { createAllocationPlan, projectRetirement } from "@/lib/allocation-engine";
import { formatINR } from "@/lib/format";
import type { EquityStrategy } from "@/lib/types";

export default function MutualFundsPage() {
  const { profile } = useProfile();

  const plan = useMemo(
    () =>
      createAllocationPlan({
        age: profile.profile_age,
        monthly_income: profile.profile_income,
        monthly_investment: profile.profile_sip,
        risk_profile: profile.profile_mf_risk as "conservative" | "moderate" | "aggressive",
        custom_equity: profile.profile_equity,
        has_emergency_fund: profile.profile_emergency_fund,
        has_insurance: profile.profile_insurance,
        equity_strategy: profile.profile_equity_strategy as EquityStrategy,
      }),
    [profile]
  );

  const retirement = projectRetirement(
    profile.profile_sip,
    profile.profile_mf_value,
    profile.profile_target_years,
    profile.profile_expected_return / 100
  );

  const pieData = Object.entries(plan.monthly_sip_breakdown).map(([name, value]) => ({
    name,
    value,
  }));

  const allAllocs = { ...plan.equity_allocations, ...plan.debt_allocations };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">📈 Mutual Fund Planner</h1>
        <p className="mt-1 text-slate-400">Equity-debt allocation · SIP breakdown · retirement projection</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="stat-box">
          <div className="num">{plan.equity_percentage}%</div>
          <div className="lbl">Equity</div>
        </div>
        <div className="stat-box">
          <div className="num">{plan.debt_percentage}%</div>
          <div className="lbl">Debt</div>
        </div>
        <div className="stat-box">
          <div className="num">{formatINR(profile.profile_sip)}</div>
          <div className="lbl">Monthly SIP</div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card">
          <h2 className="mb-3 font-semibold">SIP Allocation</h2>
          <AllocationPie data={pieData} />
        </div>

        <div className="glass-card">
          <h2 className="mb-3 font-semibold">Fund breakdown</h2>
          <div className="space-y-3">
            {Object.entries(allAllocs).map(([key, alloc]) => (
              <div key={key} className="border-b border-white/10 pb-2 text-sm">
                <div className="flex justify-between font-medium">
                  <span>{alloc.subcategory}</span>
                  <span>{alloc.percentage}% · {formatINR(alloc.amount)}</span>
                </div>
                {alloc.recommended_funds.length > 0 && (
                  <p className="mt-1 text-xs text-slate-400">
                    {alloc.recommended_funds.join(", ")}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-card">
        <h2 className="mb-3 font-semibold">Retirement / corpus projection</h2>
        <p className="text-sm text-slate-400">
          {profile.profile_target_years} years at {profile.profile_expected_return}% expected return
        </p>
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          <div>
            <p className="text-xs text-slate-500">Projected corpus</p>
            <p className="font-mono text-xl font-bold text-accent">{formatINR(retirement.corpus)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500">Total invested</p>
            <p className="font-mono text-xl">{formatINR(retirement.invested)}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500">Estimated gains</p>
            <p className="font-mono text-xl text-accent-purple">{formatINR(retirement.gains)}</p>
          </div>
        </div>
      </div>

      {plan.warnings.length > 0 && (
        <div className="space-y-2">
          {plan.warnings.map((w, i) => (
            <div key={i} className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm">
              {w}
            </div>
          ))}
        </div>
      )}

      <div className="glass-card">
        <h2 className="mb-2 font-semibold">Recommendations</h2>
        <ul className="list-inside list-disc space-y-1 text-sm text-slate-300">
          {plan.recommendations.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
