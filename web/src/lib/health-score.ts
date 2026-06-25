import type { HealthResult } from "./types";

export function computeHealthScore(params: {
  age: number;
  monthly_income: number;
  monthly_investment: number;
  has_emergency_fund: boolean;
  has_insurance: boolean;
  equity_pct: number;
}): HealthResult {
  const breakdown: Record<string, number> = {};
  const insights: string[] = [];

  const ef = params.has_emergency_fund ? 20 : 4;
  breakdown["Emergency Fund"] = ef;
  if (!params.has_emergency_fund) {
    insights.push("Build 6 months of expenses in liquid savings before aggressive investing.");
  }

  const ins = params.has_insurance ? 20 : 6;
  breakdown["Insurance"] = ins;
  if (!params.has_insurance) {
    insights.push("Term life + health cover protect your family and free you to invest confidently.");
  }

  const ratio =
    params.monthly_income > 0
      ? (params.monthly_investment / params.monthly_income) * 100
      : 0;
  let sr: number;
  if (ratio >= 30) sr = 20;
  else if (ratio >= 20) sr = 16;
  else if (ratio >= 10) sr = 12;
  else if (ratio >= 5) sr = 8;
  else {
    sr = 4;
    insights.push("Aim to invest at least 20% of take-home income via SIP.");
  }
  breakdown["Savings Rate"] = sr;

  const idealEquity = Math.max(20, Math.min(80, 100 - params.age));
  const drift = Math.abs(params.equity_pct - idealEquity);
  let alloc: number;
  if (drift <= 10) alloc = 20;
  else if (drift <= 20) alloc = 14;
  else if (drift <= 30) alloc = 8;
  else {
    alloc = 4;
    insights.push(
      `For age ${params.age}, equity near ${idealEquity.toFixed(0)}% is often appropriate — review your split.`
    );
  }
  breakdown["Asset Allocation Fit"] = alloc;

  let disc: number;
  if (params.monthly_investment >= 10000) disc = 20;
  else if (params.monthly_investment >= 5000) disc = 16;
  else if (params.monthly_investment > 0) disc = 12;
  else {
    disc = 0;
    insights.push("Start a monthly SIP — even ₹2,000 compounds powerfully over decades.");
  }
  breakdown["Investment Discipline"] = disc;

  const total = Object.values(breakdown).reduce((a, b) => a + b, 0);
  let grade: string;
  let color: string;
  if (total >= 85) [grade, color] = ["Excellent", "#00d4aa"];
  else if (total >= 70) [grade, color] = ["Strong", "#34d399"];
  else if (total >= 55) [grade, color] = ["Good", "#fbbf24"];
  else if (total >= 40) [grade, color] = ["Fair", "#fb923c"];
  else [grade, color] = ["Needs Work", "#f43f5e"];

  if (total >= 70 && insights.length === 0) {
    insights.push("You're on a solid path — stay consistent and rebalance annually.");
  }

  return { score: total, grade, color, breakdown, insights };
}
