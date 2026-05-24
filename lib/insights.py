"""AI-style advisor — rule-based insights from profile + markets."""

from __future__ import annotations

from lib.health_score import compute_health_score, HealthResult


def generate_advisor_insights(
    profile: dict,
    mood_score: int,
    mood_label: str,
    goals_gap_total: float = 0,
) -> list[dict]:
    """Return prioritized insights with category and urgency."""
    insights: list[dict] = []

    health: HealthResult = compute_health_score(
        age=profile["profile_age"],
        monthly_income=profile["profile_income"],
        monthly_investment=profile["profile_sip"],
        has_emergency_fund=profile["profile_emergency_fund"],
        has_insurance=profile["profile_insurance"],
        equity_pct=profile["profile_equity"],
    )

    if not profile["profile_emergency_fund"]:
        insights.append(
            {
                "priority": 1,
                "category": "Safety",
                "title": "Build your emergency fund first",
                "body": f"Target ₹{profile['profile_income'] * 6:,.0f} (6 months expenses) in liquid savings before aggressive equity.",
                "action": "Park 20% of SIP in liquid funds until funded.",
            }
        )

    if not profile["profile_insurance"]:
        insights.append(
            {
                "priority": 2,
                "category": "Protection",
                "title": "Close your insurance gap",
                "body": "Term cover ~10–15× annual income plus family health floater.",
                "action": "Get quotes this week — it's non-negotiable.",
            }
        )

    ideal_eq = max(20, min(80, 100 - profile["profile_age"]))
    if abs(profile["profile_equity"] - ideal_eq) > 15:
        direction = "reduce" if profile["profile_equity"] > ideal_eq else "increase"
        insights.append(
            {
                "priority": 3,
                "category": "Allocation",
                "title": f"Consider {direction}ing equity exposure",
                "body": f"At age {profile['profile_age']}, ~{ideal_eq:.0f}% equity is a common baseline. You're at {profile['profile_equity']}%.",
                "action": f"Gradually {direction} equity by 5% per year via rebalancing.",
            }
        )

    if goals_gap_total > 0:
        insights.append(
            {
                "priority": 4,
                "category": "Goals",
                "title": "Goals need more monthly funding",
                "body": f"You're ₹{goals_gap_total:,.0f}/month short across your goals.",
                "action": "Trim expenses or extend timelines — see Goal Planner.",
            }
        )

    if mood_score >= 75:
        insights.append(
            {
                "priority": 5,
                "category": "Crypto",
                "title": "Market euphoria detected",
                "body": f"Mood index at {mood_score} ({mood_label}). Historically, greed peaks precede corrections.",
                "action": "Avoid FOMO buys; stick to SIP schedule.",
            }
        )
    elif mood_score <= 25:
        insights.append(
            {
                "priority": 5,
                "category": "Crypto",
                "title": "Fear in crypto markets",
                "body": f"Mood at {mood_score} ({mood_label}). Volatility is high but SIP discipline wins long-term.",
                "action": "Continue DCA; don't try to catch the bottom.",
            }
        )

    ratio = profile["profile_sip"] / profile["profile_income"] * 100 if profile["profile_income"] else 0
    if ratio >= 25 and health.score >= 70:
        insights.append(
            {
                "priority": 6,
                "category": "Wealth",
                "title": "You're compounding well",
                "body": f"Saving {ratio:.0f}% of income with health score {health.score}/100.",
                "action": "Run Monte Carlo in Command Center to stress-test scenarios.",
            }
        )

    if profile["profile_crypto_usd"] > 0:
        crypto_inr = profile["profile_crypto_usd"] * profile["profile_usd_inr"]
        total = profile["profile_mf_value"] + crypto_inr
        if total > 0 and crypto_inr / total > 0.25:
            insights.append(
                {
                    "priority": 7,
                    "category": "Risk",
                    "title": "Crypto concentration elevated",
                    "body": f"Crypto is {crypto_inr/total*100:.0f}% of portfolio — above typical 5–15% satellite allocation.",
                    "action": "Rebalance profits into MF core holdings annually.",
                }
            )

    if not insights:
        insights.append(
            {
                "priority": 99,
                "category": "General",
                "title": "Stay the course",
                "body": "Your fundamentals look solid. Focus on consistency.",
                "action": "Review allocation quarterly; rebalance annually.",
            }
        )

    insights.sort(key=lambda x: x["priority"])
    return insights
