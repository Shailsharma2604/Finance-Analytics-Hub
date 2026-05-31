"""Best-plan engine — wealth/profit targets drive SIP, allocation, and goals."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Literal

from lib.goals import monthly_sip_for_goal
from lib.simulator import run_monte_carlo

RiskChoice = Literal["auto", "conservative", "moderate", "aggressive"]
TargetMode = Literal["wealth", "profit"]


@dataclass
class RecommendedPlan:
    target_mode: str
    wealth_target: float
    profit_target_annual: float
    target_years: int
    current_wealth: float
    required_monthly_sip: float
    recommended_sip: float
    equity_pct: int
    mf_pct: float
    crypto_pct: float
    liquid_pct: float
    risk_profile: str
    equity_strategy: str
    mf_sip: float
    crypto_sip: float
    liquid_sip: float
    expected_annual_profit: float
    median_corpus_at_horizon: float
    success_probability: float
    on_track: bool
    gap_monthly: float
    savings_rate_pct: float
    plan_grade: str
    summary: str
    actions: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _current_wealth(profile: dict) -> float:
    crypto_inr = profile["profile_crypto_usd"] * profile["profile_usd_inr"]
    return profile["profile_mf_value"] + crypto_inr


def _ideal_equity(age: int, risk: RiskChoice) -> int:
    if risk == "conservative":
        base = max(20, min(50, 100 - age - 10))
    elif risk == "moderate":
        base = max(30, min(65, 100 - age))
    elif risk == "aggressive":
        base = max(50, min(85, 110 - age))
    else:
        base = max(25, min(80, 100 - age))
    return int(base)


def _risk_profile_name(age: int, risk: RiskChoice) -> str:
    if risk != "auto":
        return risk
    if age < 35:
        return "aggressive"
    if age < 50:
        return "moderate"
    return "conservative"


def _equity_strategy(risk: str, equity_pct: int) -> str:
    if risk == "aggressive" or equity_pct >= 70:
        return "aggressive_growth"
    if risk == "moderate" or equity_pct >= 50:
        return "balanced_growth"
    if equity_pct >= 40:
        return "market_weighted"
    return "index_core"


def _wealth_from_profit(annual_profit: float, return_rate: float = 0.12) -> float:
    """Corpus that could yield ~annual_profit at given return (simplified)."""
    if return_rate <= 0:
        return annual_profit * 10
    return annual_profit / return_rate


def _max_affordable_sip(income: float, has_ef: bool) -> float:
    cap = income * 0.45
    if not has_ef:
        cap = min(cap, income * 0.25)
    return max(0, cap)


def build_best_plan(profile: dict) -> RecommendedPlan:
    """Compute optimal plan from global profile + targets."""
    mode: TargetMode = profile.get("profile_target_mode", "wealth")
    years = max(1, int(profile.get("profile_target_years", 15)))
    income = float(profile["profile_income"])
    age = int(profile["profile_age"])
    current = _current_wealth(profile)
    current_sip = float(profile["profile_sip"])
    risk_choice: RiskChoice = profile.get("profile_risk", "auto")
    return_rate = float(profile.get("profile_expected_return", 12.0)) / 100
    has_ef = profile["profile_emergency_fund"]
    has_ins = profile["profile_insurance"]

    profit_target = float(profile.get("profile_profit_target", 0))
    wealth_target = float(profile.get("profile_wealth_target", 5_000_000))

    if mode == "profit" and profit_target > 0:
        wealth_target = _wealth_from_profit(profit_target, return_rate)
    elif wealth_target <= 0 and profit_target > 0:
        wealth_target = _wealth_from_profit(profit_target, return_rate)

    required_sip = monthly_sip_for_goal(
        wealth_target, years, return_rate * 100, current_saved=current
    )

    affordable = _max_affordable_sip(income, has_ef)
    recommended_sip = min(required_sip, affordable) if affordable > 0 else required_sip
    if recommended_sip < required_sip * 0.5 and income > 0:
        recommended_sip = min(required_sip, income * 0.35)

    equity_pct = _ideal_equity(age, risk_choice)
    risk_name = _risk_profile_name(age, risk_choice)
    strategy = _equity_strategy(risk_name, equity_pct)

    if not has_ef:
        liquid_pct = 20.0
        mf_pct = (100 - equity_pct - 20) * 0.85
        crypto_pct = max(5, 100 - equity_pct - liquid_pct - mf_pct)
    else:
        liquid_pct = 5.0
        crypto_pct = 10.0 if age < 40 else 5.0
        mf_pct = 100 - equity_pct - liquid_pct - crypto_pct

    mf_pct = max(0, round(mf_pct, 1))
    crypto_pct = max(0, round(crypto_pct, 1))
    liquid_pct = max(0, round(liquid_pct, 1))

    mf_sip = round(recommended_sip * (mf_pct / 100), 0)
    crypto_sip = round(recommended_sip * (crypto_pct / 100), 0)
    liquid_sip = round(recommended_sip * (liquid_pct / 100), 0)

    sim = run_monte_carlo(recommended_sip, current, years, mean_return=return_rate, volatility=0.18)
    median = sim["final_median"]
    success_prob = float(sim.get("probability_goal") or 0)
    if wealth_target > 0:
        finals = []
        import numpy as np

        months = years * 12
        mu = return_rate / 12
        sigma = 0.18 / (12**0.5)
        for _ in range(500):
            b = current
            for _ in range(months):
                b = b * (1 + np.random.normal(mu, sigma)) + recommended_sip
            finals.append(b)
        success_prob = float(np.mean(np.array(finals) >= wealth_target))

    expected_profit = median * return_rate if median > 0 else recommended_sip * 12 * return_rate
    gap = max(0, required_sip - current_sip)
    on_track = current_sip >= required_sip * 0.92 and success_prob >= 0.55
    savings_rate = (recommended_sip / income * 100) if income else 0

    if on_track and success_prob >= 0.7:
        grade = "A — On track"
    elif success_prob >= 0.5 or gap < income * 0.1:
        grade = "B — Adjust slightly"
    else:
        grade = "C — Needs more funding"

    actions: list[str] = []
    if not has_ef:
        actions.append(f"Build ₹{income * 6:,.0f} emergency fund — allocate {liquid_pct:.0f}% of SIP to liquid funds first.")
    if not has_ins:
        actions.append("Get term + health insurance before increasing equity.")
    if gap > 0:
        actions.append(f"Raise monthly SIP by ₹{gap:,.0f} or extend horizon by {max(1, int(years * 0.15))} years.")
    if current_sip < recommended_sip:
        actions.append(f"Set SIP to ₹{recommended_sip:,.0f}/mo ({savings_rate:.0f}% of income) for your target.")
    actions.append(
        f"Use {risk_name} MF plan: {equity_pct}% equity, strategy **{strategy.replace('_', ' ')}**."
    )
    actions.append(f"Split SIP: ₹{mf_sip:,.0f} MF · ₹{crypto_sip:,.0f} crypto · ₹{liquid_sip:,.0f} liquid.")

    if mode == "profit":
        summary = (
            f"Target **₹{profit_target:,.0f}/year** profit → needs ~**₹{wealth_target:,.0f}** corpus in **{years}y**. "
            f"Recommended SIP **₹{recommended_sip:,.0f}/mo** ({grade})."
        )
    else:
        summary = (
            f"Target corpus **₹{wealth_target:,.0f}** in **{years}y** → SIP **₹{recommended_sip:,.0f}/mo** "
            f"({success_prob * 100:.0f}% Monte Carlo success, {grade})."
        )

    return RecommendedPlan(
        target_mode=mode,
        wealth_target=wealth_target,
        profit_target_annual=profit_target,
        target_years=years,
        current_wealth=current,
        required_monthly_sip=round(required_sip, 0),
        recommended_sip=round(recommended_sip, 0),
        equity_pct=equity_pct,
        mf_pct=mf_pct,
        crypto_pct=crypto_pct,
        liquid_pct=liquid_pct,
        risk_profile=risk_name,
        equity_strategy=strategy,
        mf_sip=mf_sip,
        crypto_sip=crypto_sip,
        liquid_sip=liquid_sip,
        expected_annual_profit=round(expected_profit, 0),
        median_corpus_at_horizon=round(median, 0),
        success_probability=round(success_prob, 3),
        on_track=on_track,
        gap_monthly=round(gap, 0),
        savings_rate_pct=round(savings_rate, 1),
        plan_grade=grade,
        summary=summary,
        actions=actions,
    )


def apply_plan_to_session(plan: RecommendedPlan) -> None:
    """Push recommended values into global profile + goals."""
    import streamlit as st

    st.session_state.profile_sip = int(plan.recommended_sip)
    st.session_state.profile_equity = int(plan.equity_pct)
    st.session_state.profile_risk = plan.risk_profile
    st.session_state.profile_mf_risk = plan.risk_profile
    st.session_state.profile_equity_strategy = plan.equity_strategy
    st.session_state.profile_wealth_target = plan.wealth_target
    st.session_state.profile_profit_target = plan.profit_target_annual
    st.session_state.recommended_plan = plan.to_dict()
    st.session_state.plan_applied = True

    if "goals_df" in st.session_state:
        import pandas as pd

        df = st.session_state.goals_df.copy()
        primary = "Wealth target (from profile)"
        if len(df) > 0:
            if "Goal" in df.columns:
                df.at[df.index[0], "Goal"] = primary
            if "Target (₹)" in df.columns:
                df.at[df.index[0], "Target (₹)"] = plan.wealth_target
            if "Years" in df.columns:
                df.at[df.index[0], "Years"] = plan.target_years
            if "Your SIP (₹)" in df.columns:
                df.at[df.index[0], "Your SIP (₹)"] = plan.recommended_sip
            if "Saved (₹)" in df.columns:
                df.at[df.index[0], "Saved (₹)"] = plan.current_wealth
        else:
            df = pd.DataFrame(
                [
                    {
                        "Goal": primary,
                        "Target (₹)": plan.wealth_target,
                        "Years": plan.target_years,
                        "Priority": 1,
                        "Saved (₹)": plan.current_wealth,
                        "Your SIP (₹)": plan.recommended_sip,
                    }
                ]
            )
        st.session_state.goals_df = df

    st.session_state.goals_gap_total = plan.gap_monthly


def get_recommended_plan(profile: dict) -> RecommendedPlan | None:
    import streamlit as st

    if st.session_state.get("recommended_plan"):
        d = st.session_state["recommended_plan"]
        return RecommendedPlan(**d)
    if profile.get("profile_wealth_target", 0) > 0 or profile.get("profile_profit_target", 0) > 0:
        return build_best_plan(profile)
    return None
