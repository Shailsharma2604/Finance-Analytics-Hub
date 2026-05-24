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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_profile() -> dict:
    init_profile()
    return {k: st.session_state[k] for k in PROFILE_KEYS}


def render_profile_sidebar():
    """Compact profile editor — appears on every page sidebar."""
    init_profile()
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
        st.session_state.profile_emergency_fund = st.checkbox(
            "Emergency fund", st.session_state.profile_emergency_fund, key="sb_ef"
        )
        st.session_state.profile_insurance = st.checkbox(
            "Insurance", st.session_state.profile_insurance, key="sb_ins"
        )
        if st.button("Apply across app", use_container_width=True):
            st.toast("Profile synced to all modules")

        if st.button("🎬 Load demo profile", use_container_width=True, help="For viva / presentation"):
            from lib.demo_data import load_demo_into_session

            load_demo_into_session()
            st.balloons()
            st.rerun()
