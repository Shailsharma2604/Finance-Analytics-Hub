import { monthlySipForGoal } from "./goals";
import { runMonteCarlo } from "./simulator";
import type { Profile, RecommendedPlan, RiskChoice, TargetMode } from "./types";
import { currentWealth } from "./format";

function idealEquity(age: number, risk: RiskChoice): number {
  let base: number;
  if (risk === "conservative") base = Math.max(20, Math.min(50, 100 - age - 10));
  else if (risk === "moderate") base = Math.max(30, Math.min(65, 100 - age));
  else if (risk === "aggressive") base = Math.max(50, Math.min(85, 110 - age));
  else base = Math.max(25, Math.min(80, 100 - age));
  return Math.round(base);
}

function riskProfileName(age: number, risk: RiskChoice): string {
  if (risk !== "auto") return risk;
  if (age < 35) return "aggressive";
  if (age < 50) return "moderate";
  return "conservative";
}

function equityStrategy(risk: string, equityPct: number): string {
  if (risk === "aggressive" || equityPct >= 70) return "aggressive_growth";
  if (risk === "moderate" || equityPct >= 50) return "balanced_growth";
  if (equityPct >= 40) return "market_weighted";
  return "index_core";
}

function wealthFromProfit(annualProfit: number, returnRate = 0.12): number {
  if (returnRate <= 0) return annualProfit * 10;
  return annualProfit / returnRate;
}

function maxAffordableSip(income: number, hasEf: boolean): number {
  let cap = income * 0.45;
  if (!hasEf) cap = Math.min(cap, income * 0.25);
  return Math.max(0, cap);
}

function computeSuccessProb(
  recommendedSip: number,
  current: number,
  years: number,
  wealthTarget: number,
  returnRate: number
): number {
  const months = years * 12;
  const mu = returnRate / 12;
  const sigma = 0.18 / Math.sqrt(12);
  let success = 0;
  for (let s = 0; s < 500; s++) {
    let b = current;
    for (let m = 0; m < months; m++) {
      const u1 = Math.random();
      const u2 = Math.random();
      const z = Math.sqrt(-2 * Math.log(Math.max(u1, 1e-10))) * Math.cos(2 * Math.PI * u2);
      b = b * (1 + (mu + z * sigma)) + recommendedSip;
    }
    if (b >= wealthTarget) success++;
  }
  return success / 500;
}

export function buildBestPlan(profile: Profile): RecommendedPlan {
  const mode: TargetMode = profile.profile_target_mode ?? "wealth";
  const years = Math.max(1, profile.profile_target_years);
  const income = profile.profile_income;
  const age = profile.profile_age;
  const current = currentWealth(profile);
  const currentSip = profile.profile_sip;
  const riskChoice: RiskChoice = profile.profile_risk;
  const returnRate = profile.profile_expected_return / 100;
  const hasEf = profile.profile_emergency_fund;
  const hasIns = profile.profile_insurance;

  let profitTarget = profile.profile_profit_target;
  let wealthTarget = profile.profile_wealth_target;

  if (mode === "profit" && profitTarget > 0) {
    wealthTarget = wealthFromProfit(profitTarget, returnRate);
  } else if (wealthTarget <= 0 && profitTarget > 0) {
    wealthTarget = wealthFromProfit(profitTarget, returnRate);
  }

  const requiredSip = monthlySipForGoal(wealthTarget, years, returnRate * 100, current);
  const affordable = maxAffordableSip(income, hasEf);
  let recommendedSip =
    affordable > 0 ? Math.min(requiredSip, affordable) : requiredSip;
  if (recommendedSip < requiredSip * 0.5 && income > 0) {
    recommendedSip = Math.min(requiredSip, income * 0.35);
  }

  const equityPct = idealEquity(age, riskChoice);
  const riskName = riskProfileName(age, riskChoice);
  const strategy = equityStrategy(riskName, equityPct);

  let liquidPct: number;
  let mfPct: number;
  let cryptoPct: number;

  if (!hasEf) {
    liquidPct = 20;
    mfPct = (100 - equityPct - 20) * 0.85;
    cryptoPct = Math.max(5, 100 - equityPct - liquidPct - mfPct);
  } else {
    liquidPct = 5;
    cryptoPct = age < 40 ? 10 : 5;
    mfPct = 100 - equityPct - liquidPct - cryptoPct;
  }

  mfPct = Math.max(0, Math.round(mfPct * 10) / 10);
  cryptoPct = Math.max(0, Math.round(cryptoPct * 10) / 10);
  liquidPct = Math.max(0, Math.round(liquidPct * 10) / 10);

  const mfSip = Math.round(recommendedSip * (mfPct / 100));
  const cryptoSip = Math.round(recommendedSip * (cryptoPct / 100));
  const liquidSip = Math.round(recommendedSip * (liquidPct / 100));

  const sim = runMonteCarlo(recommendedSip, current, years, returnRate, 0.18);
  const median = sim.final_median;
  const successProb =
    wealthTarget > 0
      ? computeSuccessProb(recommendedSip, current, years, wealthTarget, returnRate)
      : 0;

  const expectedProfit =
    median > 0 ? median * returnRate : recommendedSip * 12 * returnRate;
  const gap = Math.max(0, requiredSip - currentSip);
  const onTrack = currentSip >= requiredSip * 0.92 && successProb >= 0.55;
  const savingsRate = income ? (recommendedSip / income) * 100 : 0;

  let grade: string;
  if (onTrack && successProb >= 0.7) grade = "A — On track";
  else if (successProb >= 0.5 || gap < income * 0.1) grade = "B — Adjust slightly";
  else grade = "C — Needs more funding";

  const actions: string[] = [];
  if (!hasEf) {
    actions.push(
      `Build ₹${(income * 6).toLocaleString("en-IN")} emergency fund — allocate ${liquidPct.toFixed(0)}% of SIP to liquid funds first.`
    );
  }
  if (!hasIns) {
    actions.push("Get term + health insurance before increasing equity.");
  }
  if (gap > 0) {
    actions.push(
      `Raise monthly SIP by ₹${gap.toLocaleString("en-IN")} or extend horizon by ${Math.max(1, Math.round(years * 0.15))} years.`
    );
  }
  if (currentSip < recommendedSip) {
    actions.push(
      `Set SIP to ₹${Math.round(recommendedSip).toLocaleString("en-IN")}/mo (${savingsRate.toFixed(0)}% of income) for your target.`
    );
  }
  actions.push(
    `Use ${riskName} MF plan: ${equityPct}% equity, strategy ${strategy.replace(/_/g, " ")}.`
  );
  actions.push(
    `Split SIP: ₹${mfSip.toLocaleString("en-IN")} MF · ₹${cryptoSip.toLocaleString("en-IN")} crypto · ₹${liquidSip.toLocaleString("en-IN")} liquid.`
  );

  const summary =
    mode === "profit"
      ? `Target ₹${profitTarget.toLocaleString("en-IN")}/year profit → needs ~₹${wealthTarget.toLocaleString("en-IN")} corpus in ${years}y. Recommended SIP ₹${Math.round(recommendedSip).toLocaleString("en-IN")}/mo (${grade}).`
      : `Target corpus ₹${wealthTarget.toLocaleString("en-IN")} in ${years}y → SIP ₹${Math.round(recommendedSip).toLocaleString("en-IN")}/mo (${(successProb * 100).toFixed(0)}% Monte Carlo success, ${grade}).`;

  return {
    target_mode: mode,
    wealth_target: wealthTarget,
    profit_target_annual: profitTarget,
    target_years: years,
    current_wealth: current,
    required_monthly_sip: Math.round(requiredSip),
    recommended_sip: Math.round(recommendedSip),
    equity_pct: equityPct,
    mf_pct: mfPct,
    crypto_pct: cryptoPct,
    liquid_pct: liquidPct,
    risk_profile: riskName,
    equity_strategy: strategy,
    mf_sip: mfSip,
    crypto_sip: cryptoSip,
    liquid_sip: liquidSip,
    expected_annual_profit: Math.round(expectedProfit),
    median_corpus_at_horizon: Math.round(median),
    success_probability: Math.round(successProb * 1000) / 1000,
    on_track: onTrack,
    gap_monthly: Math.round(gap),
    savings_rate_pct: Math.round(savingsRate * 10) / 10,
    plan_grade: grade,
    summary,
    actions,
  };
}
