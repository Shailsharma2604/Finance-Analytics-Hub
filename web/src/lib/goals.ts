import type { GoalPlan } from "./types";

export function monthlySipForGoal(
  target: number,
  years: number,
  annualReturn = 0.12,
  currentSaved = 0
): number {
  const months = Math.max(years * 12, 1);
  const r = annualReturn > 1 ? annualReturn / 12 / 100 : annualReturn / 12;
  const fvExisting = currentSaved * Math.pow(1 + r, months);
  const remaining = Math.max(0, target - fvExisting);
  if (r === 0) return remaining / months;
  return (remaining * r) / ((Math.pow(1 + r, months) - 1) * (1 + r));
}

export function assetForHorizon(years: number): string {
  if (years <= 3) return "Debt / FD / Liquid funds";
  if (years <= 7) return "Hybrid (40% equity max)";
  return "Equity-heavy (index + diversified)";
}

export function planGoal(
  name: string,
  target: number,
  years: number,
  priority: number,
  currentSaved: number,
  allocatedSip: number,
  annualReturn = 12
): GoalPlan {
  const required = monthlySipForGoal(target, years, annualReturn, currentSaved);
  const gap = Math.max(0, required - allocatedSip);
  return {
    name,
    target,
    years,
    priority,
    required_monthly_sip: Math.round(required),
    recommended_asset: assetForHorizon(years),
    on_track: allocatedSip >= required * 0.95,
    gap_monthly: Math.round(gap),
  };
}
