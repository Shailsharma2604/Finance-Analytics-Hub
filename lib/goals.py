"""Financial goal planning — SIP required, feasibility, allocation hints."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GoalPlan:
    name: str
    target: float
    years: int
    priority: int
    required_monthly_sip: float
    recommended_asset: str
    on_track: bool
    gap_monthly: float


def monthly_sip_for_goal(
    target: float,
    years: int,
    annual_return: float = 0.12,
    current_saved: float = 0.0,
) -> float:
    """PMT: monthly SIP needed to reach target."""
    months = max(years * 12, 1)
    r = annual_return / 12 / 100 if annual_return > 1 else annual_return / 12
    fv_existing = current_saved * ((1 + r) ** months)
    remaining = max(0, target - fv_existing)
    if r == 0:
        return remaining / months
    return remaining * r / (((1 + r) ** months - 1) * (1 + r))


def asset_for_horizon(years: int) -> str:
    if years <= 3:
        return "Debt / FD / Liquid funds"
    if years <= 7:
        return "Hybrid (40% equity max)"
    return "Equity-heavy (index + diversified)"


def plan_goal(
    name: str,
    target: float,
    years: int,
    priority: int,
    current_saved: float,
    allocated_sip: float,
    annual_return: float = 12.0,
) -> GoalPlan:
    required = monthly_sip_for_goal(target, years, annual_return, current_saved)
    gap = max(0, required - allocated_sip)
    return GoalPlan(
        name=name,
        target=target,
        years=years,
        priority=priority,
        required_monthly_sip=round(required, 0),
        recommended_asset=asset_for_horizon(years),
        on_track=allocated_sip >= required * 0.95,
        gap_monthly=round(gap, 0),
    )
