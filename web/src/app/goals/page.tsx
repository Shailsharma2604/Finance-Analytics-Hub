"use client";

import { useMemo } from "react";
import { useProfile } from "@/context/ProfileContext";
import { planGoal } from "@/lib/goals";
import { probabilityOfReachingGoal } from "@/lib/simulator";
import { formatINR } from "@/lib/format";
import type { GoalRow } from "@/lib/types";

export default function GoalsPage() {
  const { goals, setGoals, profile } = useProfile();

  const plans = useMemo(
    () =>
      goals.map((g) =>
        planGoal(g.goal, g.target, g.years, g.priority, g.saved, g.sip, profile.profile_expected_return)
      ),
    [goals, profile.profile_expected_return]
  );

  const totalGap = plans.reduce((s, p) => s + p.gap_monthly, 0);
  const totalRequired = plans.reduce((s, p) => s + p.required_monthly_sip, 0);

  const updateGoal = (id: string, patch: Partial<GoalRow>) => {
    setGoals(goals.map((g) => (g.id === id ? { ...g, ...patch } : g)));
  };

  const addGoal = () => {
    const id = String(Date.now());
    setGoals([
      ...goals,
      {
        id,
        goal: "New goal",
        target: 1_000_000,
        years: 10,
        priority: goals.length + 1,
        saved: 0,
        sip: 5_000,
      },
    ]);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">🎯 Goal Planner</h1>
        <p className="mt-1 text-slate-400">Multi-goal SIP · success probability · asset hints</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="stat-box">
          <div className="num">{goals.length}</div>
          <div className="lbl">Goals</div>
        </div>
        <div className="stat-box">
          <div className="num">{formatINR(totalRequired)}</div>
          <div className="lbl">Required SIP/mo</div>
        </div>
        <div className="stat-box">
          <div className="num">{formatINR(totalGap)}</div>
          <div className="lbl">Gap to close</div>
        </div>
      </div>

      <button type="button" onClick={addGoal} className="btn-secondary">
        + Add goal
      </button>

      <div className="space-y-4">
        {goals.map((g, i) => {
          const plan = plans[i];
          const prob = probabilityOfReachingGoal(
            g.sip,
            g.saved,
            g.years,
            g.target,
            profile.profile_expected_return / 100
          );
          return (
            <div key={g.id} className="glass-card space-y-3">
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                <label className="text-sm">
                  Goal name
                  <input
                    className="input-field mt-1"
                    value={g.goal}
                    onChange={(e) => updateGoal(g.id, { goal: e.target.value })}
                  />
                </label>
                <label className="text-sm">
                  Target (₹)
                  <input
                    type="number"
                    className="input-field mt-1"
                    value={g.target}
                    onChange={(e) => updateGoal(g.id, { target: Number(e.target.value) })}
                  />
                </label>
                <label className="text-sm">
                  Years
                  <input
                    type="number"
                    className="input-field mt-1"
                    value={g.years}
                    onChange={(e) => updateGoal(g.id, { years: Number(e.target.value) })}
                  />
                </label>
                <label className="text-sm">
                  Your SIP (₹)
                  <input
                    type="number"
                    className="input-field mt-1"
                    value={g.sip}
                    onChange={(e) => updateGoal(g.id, { sip: Number(e.target.value) })}
                  />
                </label>
              </div>

              <div className="grid gap-3 text-sm sm:grid-cols-4">
                <div>
                  <p className="text-slate-500">Required SIP</p>
                  <p className="font-mono font-semibold">{formatINR(plan.required_monthly_sip)}</p>
                </div>
                <div>
                  <p className="text-slate-500">Recommended asset</p>
                  <p>{plan.recommended_asset}</p>
                </div>
                <div>
                  <p className="text-slate-500">On track</p>
                  <p className={plan.on_track ? "text-accent" : "text-amber-400"}>
                    {plan.on_track ? "Yes" : `Gap ${formatINR(plan.gap_monthly)}`}
                  </p>
                </div>
                <div>
                  <p className="text-slate-500">MC success prob.</p>
                  <p className="font-mono">{(prob * 100).toFixed(0)}%</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
