import type { Profile } from "./types";
import { buildBestPlan } from "./plan-engine";

export const DEMO_PROFILE: Partial<Profile> = {
  profile_age: 22,
  profile_income: 45_000,
  profile_sip: 12_000,
  profile_equity: 75,
  profile_mf_value: 185_000,
  profile_crypto_usd: 850,
  profile_emergency_fund: true,
  profile_insurance: false,
  profile_usd_inr: 83.5,
  profile_wealth_target: 3_000_000,
  profile_profit_target: 0,
  profile_target_years: 12,
  profile_target_mode: "wealth",
  profile_risk: "aggressive",
  profile_expected_return: 12,
};

export function applyDemoProfile(base: Profile): Profile {
  const merged = { ...base, ...DEMO_PROFILE } as Profile;
  const plan = buildBestPlan(merged);
  return {
    ...merged,
    profile_sip: plan.recommended_sip,
    profile_equity: plan.equity_pct,
    profile_risk: plan.risk_profile as Profile["profile_risk"],
    profile_mf_risk: plan.risk_profile,
    profile_equity_strategy: plan.equity_strategy as Profile["profile_equity_strategy"],
    plan_applied: true,
    recommended_plan: plan,
  };
}
