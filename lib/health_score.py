"""Financial health score — holistic readiness metric (0–100)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HealthResult:
    score: int
    grade: str
    color: str
    breakdown: dict[str, int]
    insights: list[str]


def compute_health_score(
    *,
    age: int,
    monthly_income: float,
    monthly_investment: float,
    has_emergency_fund: bool,
    has_insurance: bool,
    equity_pct: float,
) -> HealthResult:
    """Score financial readiness across five pillars (20 pts each)."""
    breakdown: dict[str, int] = {}
    insights: list[str] = []

    # Emergency fund (20)
    ef = 20 if has_emergency_fund else 4
    breakdown["Emergency Fund"] = ef
    if not has_emergency_fund:
        insights.append("Build 6 months of expenses in liquid savings before aggressive investing.")

    # Insurance (20)
    ins = 20 if has_insurance else 6
    breakdown["Insurance"] = ins
    if not has_insurance:
        insights.append("Term life + health cover protect your family and free you to invest confidently.")

    # Savings rate (20)
    ratio = (monthly_investment / monthly_income * 100) if monthly_income > 0 else 0
    if ratio >= 30:
        sr = 20
    elif ratio >= 20:
        sr = 16
    elif ratio >= 10:
        sr = 12
    elif ratio >= 5:
        sr = 8
    else:
        sr = 4
        insights.append("Aim to invest at least 20% of take-home income via SIP.")
    breakdown["Savings Rate"] = sr

    # Age-appropriate allocation (20)
    ideal_equity = max(20, min(80, 100 - age))
    drift = abs(equity_pct - ideal_equity)
    if drift <= 10:
        alloc = 20
    elif drift <= 20:
        alloc = 14
    elif drift <= 30:
        alloc = 8
    else:
        alloc = 4
        insights.append(f"For age {age}, equity near {ideal_equity:.0f}% is often appropriate — review your split.")
    breakdown["Asset Allocation Fit"] = alloc

    # Investment discipline (20) — consistency proxy
    if monthly_investment >= 10000:
        disc = 20
    elif monthly_investment >= 5000:
        disc = 16
    elif monthly_investment > 0:
        disc = 12
    else:
        disc = 0
        insights.append("Start a monthly SIP — even ₹2,000 compounds powerfully over decades.")
    breakdown["Investment Discipline"] = disc

    total = sum(breakdown.values())
    if total >= 85:
        grade, color = "Excellent", "#00d4aa"
    elif total >= 70:
        grade, color = "Strong", "#34d399"
    elif total >= 55:
        grade, color = "Good", "#fbbf24"
    elif total >= 40:
        grade, color = "Fair", "#fb923c"
    else:
        grade, color = "Needs Work", "#f43f5e"

    if total >= 70 and not insights:
        insights.append("You're on a solid path — stay consistent and rebalance annually.")

    return HealthResult(
        score=total,
        grade=grade,
        color=color,
        breakdown=breakdown,
        insights=insights,
    )
