import { buildBestPlan } from "./plan-engine";
import { computeHealthScore } from "./health-score";
import type { AdvisorInsight, Profile } from "./types";
import { currentWealth } from "./format";

export function generateAdvisorInsights(
  profile: Profile,
  moodScore: number,
  moodLabel: string,
  goalsGapTotal = 0
): AdvisorInsight[] {
  const insights: AdvisorInsight[] = [];

  const plan =
    profile.recommended_plan ?? buildBestPlan(profile);

  if (plan.wealth_target > 0 || plan.profit_target_annual > 0) {
    insights.push({
      priority: 0,
      category: "Best Plan",
      title: `Recommended plan — ${plan.plan_grade}`,
      body: plan.summary,
      action: plan.actions.slice(0, 2).join(" · "),
    });
    if (plan.gap_monthly > 0) {
      insights.push({
        priority: 1,
        category: "Target",
        title: "Close the gap to your profit/wealth target",
        body: `Need ₹${plan.required_monthly_sip.toLocaleString("en-IN")}/mo SIP; you invest ₹${profile.profile_sip.toLocaleString("en-IN")}/mo.`,
        action: `Increase SIP by ₹${plan.gap_monthly.toLocaleString("en-IN")} or open Profile & Plan to re-apply.`,
      });
    }
  }

  const health = computeHealthScore({
    age: profile.profile_age,
    monthly_income: profile.profile_income,
    monthly_investment: profile.profile_sip,
    has_emergency_fund: profile.profile_emergency_fund,
    has_insurance: profile.profile_insurance,
    equity_pct: profile.profile_equity,
  });

  if (!profile.profile_emergency_fund) {
    insights.push({
      priority: 1,
      category: "Safety",
      title: "Build your emergency fund first",
      body: `Target ₹${(profile.profile_income * 6).toLocaleString("en-IN")} (6 months expenses) in liquid savings before aggressive equity.`,
      action: "Park 20% of SIP in liquid funds until funded.",
    });
  }

  if (!profile.profile_insurance) {
    insights.push({
      priority: 2,
      category: "Protection",
      title: "Close your insurance gap",
      body: "Term cover ~10–15× annual income plus family health floater.",
      action: "Get quotes this week — it's non-negotiable.",
    });
  }

  const idealEq = Math.max(20, Math.min(80, 100 - profile.profile_age));
  if (Math.abs(profile.profile_equity - idealEq) > 15) {
    const direction = profile.profile_equity > idealEq ? "reduce" : "increase";
    insights.push({
      priority: 3,
      category: "Allocation",
      title: `Consider ${direction}ing equity exposure`,
      body: `At age ${profile.profile_age}, ~${idealEq.toFixed(0)}% equity is a common baseline. You're at ${profile.profile_equity}%.`,
      action: `Gradually ${direction} equity by 5% per year via rebalancing.`,
    });
  }

  if (goalsGapTotal > 0) {
    insights.push({
      priority: 4,
      category: "Goals",
      title: "Goals need more monthly funding",
      body: `You're ₹${goalsGapTotal.toLocaleString("en-IN")}/month short across your goals.`,
      action: "Trim expenses or extend timelines — see Goal Planner.",
    });
  }

  if (moodScore >= 75) {
    insights.push({
      priority: 5,
      category: "Crypto",
      title: "Market euphoria detected",
      body: `Mood index at ${moodScore} (${moodLabel}). Historically, greed peaks precede corrections.`,
      action: "Avoid FOMO buys; stick to SIP schedule.",
    });
  } else if (moodScore <= 25) {
    insights.push({
      priority: 5,
      category: "Crypto",
      title: "Fear in crypto markets",
      body: `Mood at ${moodScore} (${moodLabel}). Volatility is high but SIP discipline wins long-term.`,
      action: "Continue DCA; don't try to catch the bottom.",
    });
  }

  const ratio =
    profile.profile_income > 0
      ? (profile.profile_sip / profile.profile_income) * 100
      : 0;
  if (ratio >= 25 && health.score >= 70) {
    insights.push({
      priority: 6,
      category: "Wealth",
      title: "You're compounding well",
      body: `Saving ${ratio.toFixed(0)}% of income with health score ${health.score}/100.`,
      action: "Run Monte Carlo in Command Center to stress-test scenarios.",
    });
  }

  if (profile.profile_crypto_usd > 0) {
    const cryptoInr = profile.profile_crypto_usd * profile.profile_usd_inr;
    const total = currentWealth(profile);
    if (total > 0 && cryptoInr / total > 0.25) {
      insights.push({
        priority: 7,
        category: "Risk",
        title: "Crypto concentration elevated",
        body: `Crypto is ${((cryptoInr / total) * 100).toFixed(0)}% of portfolio — above typical 5–15% satellite allocation.`,
        action: "Rebalance profits into MF core holdings annually.",
      });
    }
  }

  if (insights.length === 0) {
    insights.push({
      priority: 99,
      category: "General",
      title: "Stay the course",
      body: "Your fundamentals look solid. Focus on consistency.",
      action: "Review allocation quarterly; rebalance annually.",
    });
  }

  insights.sort((a, b) => a.priority - b.priority);
  return insights;
}
