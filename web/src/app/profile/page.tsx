"use client";

import { useProfile } from "@/context/ProfileContext";
import { buildBestPlan } from "@/lib/plan-engine";
import { formatINR } from "@/lib/format";
import type { RiskChoice, TargetMode } from "@/lib/types";

export default function ProfilePage() {
  const { profile, updateProfile, applyBestPlan, loadDemo } = useProfile();

  const preview = buildBestPlan(profile);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">⚙️ Profile & Best Plan</h1>
        <p className="mt-1 text-slate-400">Set targets — SIP & allocation sync across all modules</p>
      </div>

      <div className="flex flex-wrap gap-3">
        <button type="button" onClick={applyBestPlan} className="btn-primary">
          🚀 Apply best plan
        </button>
        <button type="button" onClick={loadDemo} className="btn-secondary">
          🎬 Load demo profile
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="glass-card space-y-4">
          <h2 className="font-semibold">Financial profile</h2>

          <label className="block text-sm">
            Age
            <input
              type="number"
              className="input-field mt-1"
              value={profile.profile_age}
              onChange={(e) => updateProfile({ profile_age: Number(e.target.value) })}
            />
          </label>

          <label className="block text-sm">
            Monthly income (₹)
            <input
              type="number"
              className="input-field mt-1"
              value={profile.profile_income}
              onChange={(e) => updateProfile({ profile_income: Number(e.target.value) })}
            />
          </label>

          <label className="block text-sm">
            Monthly SIP (₹)
            <input
              type="number"
              className="input-field mt-1"
              value={profile.profile_sip}
              onChange={(e) => updateProfile({ profile_sip: Number(e.target.value) })}
            />
          </label>

          <label className="block text-sm">
            Equity % target
            <input
              type="range"
              min={0}
              max={100}
              className="mt-1 w-full"
              value={profile.profile_equity}
              onChange={(e) => updateProfile({ profile_equity: Number(e.target.value) })}
            />
            <span className="text-accent">{profile.profile_equity}%</span>
          </label>

          <label className="block text-sm">
            MF corpus (₹)
            <input
              type="number"
              className="input-field mt-1"
              value={profile.profile_mf_value}
              onChange={(e) => updateProfile({ profile_mf_value: Number(e.target.value) })}
            />
          </label>

          <label className="block text-sm">
            Crypto holdings (USD)
            <input
              type="number"
              className="input-field mt-1"
              value={profile.profile_crypto_usd}
              onChange={(e) => updateProfile({ profile_crypto_usd: Number(e.target.value) })}
            />
          </label>

          <div className="flex gap-4">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={profile.profile_emergency_fund}
                onChange={(e) => updateProfile({ profile_emergency_fund: e.target.checked })}
              />
              Emergency fund
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={profile.profile_insurance}
                onChange={(e) => updateProfile({ profile_insurance: e.target.checked })}
              />
              Insurance
            </label>
          </div>
        </div>

        <div className="glass-card space-y-4">
          <h2 className="font-semibold">Targets</h2>

          <label className="block text-sm">
            Target mode
            <select
              className="input-field mt-1"
              value={profile.profile_target_mode}
              onChange={(e) => updateProfile({ profile_target_mode: e.target.value as TargetMode })}
            >
              <option value="wealth">Wealth (corpus)</option>
              <option value="profit">Profit (annual)</option>
            </select>
          </label>

          {profile.profile_target_mode === "profit" ? (
            <label className="block text-sm">
              Annual profit target (₹)
              <input
                type="number"
                className="input-field mt-1"
                value={profile.profile_profit_target}
                onChange={(e) => updateProfile({ profile_profit_target: Number(e.target.value) })}
              />
            </label>
          ) : (
            <label className="block text-sm">
              Wealth target (₹)
              <input
                type="number"
                className="input-field mt-1"
                value={profile.profile_wealth_target}
                onChange={(e) => updateProfile({ profile_wealth_target: Number(e.target.value) })}
              />
            </label>
          )}

          <label className="block text-sm">
            Years to target
            <input
              type="range"
              min={3}
              max={40}
              className="mt-1 w-full"
              value={profile.profile_target_years}
              onChange={(e) => updateProfile({ profile_target_years: Number(e.target.value) })}
            />
            <span>{profile.profile_target_years} years</span>
          </label>

          <label className="block text-sm">
            Risk profile
            <select
              className="input-field mt-1"
              value={profile.profile_risk}
              onChange={(e) => updateProfile({ profile_risk: e.target.value as RiskChoice })}
            >
              <option value="auto">Auto (age-based)</option>
              <option value="conservative">Conservative</option>
              <option value="moderate">Moderate</option>
              <option value="aggressive">Aggressive</option>
            </select>
          </label>

          <label className="block text-sm">
            Expected return (%/yr)
            <input
              type="number"
              step="0.5"
              className="input-field mt-1"
              value={profile.profile_expected_return}
              onChange={(e) => updateProfile({ profile_expected_return: Number(e.target.value) })}
            />
          </label>
        </div>
      </div>

      <div className="glass-card">
        <h2 className="mb-2 font-semibold">Plan preview — {preview.plan_grade}</h2>
        <p className="text-sm text-slate-300">{preview.summary}</p>
        <div className="mt-4 grid gap-3 sm:grid-cols-4 text-sm">
          <div>
            <p className="text-slate-500">Recommended SIP</p>
            <p className="font-mono font-bold text-accent">{formatINR(preview.recommended_sip)}</p>
          </div>
          <div>
            <p className="text-slate-500">Success probability</p>
            <p className="font-mono">{(preview.success_probability * 100).toFixed(0)}%</p>
          </div>
          <div>
            <p className="text-slate-500">Equity allocation</p>
            <p className="font-mono">{preview.equity_pct}%</p>
          </div>
          <div>
            <p className="text-slate-500">Median corpus</p>
            <p className="font-mono">{formatINR(preview.median_corpus_at_horizon)}</p>
          </div>
        </div>
        <ul className="mt-4 list-inside list-disc space-y-1 text-sm text-slate-400">
          {preview.actions.map((a, i) => (
            <li key={i}>{a}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
