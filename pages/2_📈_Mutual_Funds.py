"""Mutual Fund Asset Allocation — embedded planner."""

import sys
from pathlib import Path

import streamlit as st

# Add MF package to path
MF_ROOT = Path(__file__).resolve().parent.parent / "MutualFunds-Allocation-Planner-main" / "MutualFunds-Allocation-Planner-main"
if str(MF_ROOT) not in sys.path:
    sys.path.insert(0, str(MF_ROOT))

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

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
