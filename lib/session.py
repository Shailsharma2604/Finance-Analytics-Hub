"""Global profile — syncs across all pages via session state."""

from __future__ import annotations

import streamlit as st


PROFILE_KEYS = (
    "profile_age",
    "profile_income",
    "profile_sip",
    "profile_equity",
    "profile_mf_value",
    "profile_crypto_usd",
    "profile_emergency_fund",
    "profile_insurance",
    "profile_usd_inr",
    "profile_wealth_target",
    "profile_profit_target",
    "profile_target_years",
    "profile_target_mode",
    "profile_risk",
    "profile_expected_return",
    "profile_mf_risk",
    "profile_equity_strategy",
)


def init_profile():
    defaults = {
        "profile_age": 30,
        "profile_income": 100_000,
        "profile_sip": 25_000,
        "profile_equity": 65,
        "profile_mf_value": 500_000,
        "profile_crypto_usd": 2_500.0,
        "profile_emergency_fund": False,
        "profile_insurance": False,
        "profile_usd_inr": 83.0,
        "profile_wealth_target": 5_000_000,
        "profile_profit_target": 0,
        "profile_target_years": 15,
        "profile_target_mode": "wealth",
        "profile_risk": "auto",
        "profile_expected_return": 12.0,
        "profile_mf_risk": "moderate",
        "profile_equity_strategy": "balanced_growth",
        "plan_applied": False,
        "recommended_plan": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_profile() -> dict:
    init_profile()
    return {k: st.session_state[k] for k in PROFILE_KEYS}


def apply_recommended_plan():
    """Recalculate and apply best plan from current profile."""
    from lib.plan_engine import build_best_plan, apply_plan_to_session

    plan = build_best_plan(get_profile())
    apply_plan_to_session(plan)


def render_plan_sidebar_summary():
    """Compact active-plan strip in sidebar."""
    if not st.session_state.get("plan_applied") or not st.session_state.get("recommended_plan"):
        return
    p = st.session_state["recommended_plan"]
    st.sidebar.markdown(
        f"""
        <div style="background:rgba(0,212,170,0.12);border:1px solid rgba(0,212,170,0.35);
        border-radius:10px;padding:0.6rem;margin:0.5rem 0;font-size:0.8rem;">
        <strong style="color:#00d4aa;">Active plan</strong><br>
        <span style="color:#cbd5e1;">SIP ₹{p['recommended_sip']:,.0f} · {p['equity_pct']}% equity</span><br>
        <span style="color:#94a3b8;">{p['plan_grade']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_sidebar():
    """Compact profile editor — appears on every page sidebar."""
    init_profile()
    render_plan_sidebar_summary()

    with st.sidebar.expander("👤 Your Financial Profile", expanded=False):
        st.session_state.profile_age = st.number_input(
            "Age", 18, 75, int(st.session_state.profile_age), key="sb_age"
        )
        st.session_state.profile_income = st.number_input(
            "Monthly income (₹)",
            0,
            5_000_000,
            int(st.session_state.profile_income),
            step=10_000,
            key="sb_income",
        )
        st.session_state.profile_sip = st.number_input(
            "Monthly SIP (₹)",
            0,
            500_000,
            int(st.session_state.profile_sip),
            step=5_000,
            key="sb_sip",
        )
        st.session_state.profile_equity = st.slider(
            "Equity %",
            0,
            100,
            int(st.session_state.profile_equity),
            key="sb_equity",
        )

        mode = st.session_state.profile_target_mode
        if mode == "profit":
            st.session_state.profile_profit_target = st.number_input(
                "Target profit / year (₹)",
                0,
                5_000_000,
                int(st.session_state.profile_profit_target),
                step=50_000,
                key="sb_profit",
            )
        else:
            st.session_state.profile_wealth_target = st.number_input(
                "Target corpus (₹)",
                0,
                50_000_000,
                int(st.session_state.profile_wealth_target),
                step=100_000,
                key="sb_wealth",
            )

        st.session_state.profile_target_years = st.slider(
            "Years to target",
            3,
            40,
            int(st.session_state.profile_target_years),
            key="sb_years",
        )

        st.session_state.profile_emergency_fund = st.checkbox(
            "Emergency fund", st.session_state.profile_emergency_fund, key="sb_ef"
        )
        st.session_state.profile_insurance = st.checkbox(
            "Insurance", st.session_state.profile_insurance, key="sb_ins"
        )

        if st.button("🚀 Apply best plan", use_container_width=True, type="primary"):
            apply_recommended_plan()
            st.toast("Best plan applied across all modules")
            st.rerun()

        if st.button("Open full Profile & Plan", use_container_width=True):
            st.switch_page("pages/7_⚙️_Profile_and_Plan.py")

        if st.button("🎬 Load demo profile", use_container_width=True, help="For viva / presentation"):
            from lib.demo_data import load_demo_into_session

            load_demo_into_session()
            st.balloons()
            st.rerun()
