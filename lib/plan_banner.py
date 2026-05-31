"""Reusable UI banner for active recommended plan."""

from __future__ import annotations

import streamlit as st

from lib.plan_engine import get_recommended_plan
from lib.session import get_profile


def render_active_plan_banner():
    plan = get_recommended_plan(get_profile())
    if not plan:
        return
    applied = st.session_state.get("plan_applied", False)
    badge = "✅ Active" if applied else "📐 Preview"
    st.markdown(
        f"""
        <div class="glass-card" style="margin-bottom:1rem;">
        <span class="capstone-ribbon">{badge} · Best Plan</span>
        <p style="color:#f1f5f9;margin:0.5rem 0 0;">{plan.summary}</p>
        <p style="color:#94a3b8;font-size:0.85rem;margin:0.25rem 0;">
        SIP split: MF ₹{plan.mf_sip:,.0f} · Crypto ₹{plan.crypto_sip:,.0f} · Liquid ₹{plan.liquid_sip:,.0f}
        · {plan.risk_profile.title()} · {plan.equity_pct}% equity
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
