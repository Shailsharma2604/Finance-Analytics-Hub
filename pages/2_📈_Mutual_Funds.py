"""Mutual Fund Asset Allocation — embedded planner."""

import sys
from pathlib import Path

import streamlit as st

# Add MF package to path
MF_ROOT = Path(__file__).resolve().parent.parent / "MutualFunds-Allocation-Planner-main" / "MutualFunds-Allocation-Planner-main"
if str(MF_ROOT) not in sys.path:
    sys.path.insert(0, str(MF_ROOT))

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.plan_banner import render_active_plan_banner

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

render_active_plan_banner()
profile = get_profile()

# Seed MF planner sidebar from global hub profile
st.session_state.setdefault("mf_age", int(profile["profile_age"]))
st.session_state.setdefault("mf_monthly_income", int(profile["profile_income"]))
st.session_state.setdefault("mf_monthly_investment", int(profile["profile_sip"]))
st.session_state.setdefault("mf_emergency_fund", bool(profile["profile_emergency_fund"]))
st.session_state.setdefault("mf_insurance", bool(profile["profile_insurance"]))
st.session_state.setdefault("risk_profile", profile.get("profile_mf_risk", "moderate"))
st.session_state.setdefault(
    "equity_strategy", profile.get("profile_equity_strategy", "balanced_growth")
)

if st.session_state.get("plan_applied"):
    st.info(
        f"**Use in MF sidebar:** Age {profile['profile_age']}, SIP ₹{profile['profile_sip']:,.0f}, "
        f"Risk **{profile.get('profile_mf_risk', 'moderate').title()}**, Equity **{profile['profile_equity']}%**, "
        f"Strategy **{profile.get('profile_equity_strategy', 'balanced_growth').replace('_', ' ').title()}** — "
        f"then click **Generate Plan**."
    )

st.markdown(
    """
    <h1 class="hero-title" style="font-size:2.2rem;">Mutual Fund Planner</h1>
    <p class="hero-sub">Personalized equity-debt split, SIP breakdown, and rebalancing triggers.</p>
    """,
    unsafe_allow_html=True,
)

# Import and run the existing app main()
from streamlit_app import main as mf_main

mf_main()
