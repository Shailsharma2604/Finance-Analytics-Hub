"""One-click demo profile for viva / presentation."""

DEMO_PROFILE = {
    "profile_age": 22,
    "profile_income": 45_000,
    "profile_sip": 12_000,
    "profile_equity": 75,
    "profile_mf_value": 185_000,
    "profile_crypto_usd": 850.0,
    "profile_emergency_fund": True,
    "profile_insurance": False,
    "profile_usd_inr": 83.5,
    "profile_wealth_target": 3_000_000,
    "profile_profit_target": 0,
    "profile_target_years": 12,
    "profile_target_mode": "wealth",
    "profile_risk": "aggressive",
    "profile_expected_return": 12.0,
}


def load_demo_into_session():
    import streamlit as st

    from lib.plan_engine import build_best_plan, apply_plan_to_session
    from lib.session import get_profile

    for k, v in DEMO_PROFILE.items():
        st.session_state[k] = v
    st.session_state.demo_loaded = True
    apply_plan_to_session(build_best_plan(get_profile()))
