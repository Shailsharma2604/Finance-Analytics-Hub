"""Profile & Plan — set profit/wealth targets; auto-sync across the app."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.plan_engine import build_best_plan, apply_plan_to_session, get_recommended_plan
from lib.health_score import compute_health_score
from lib.simulator import run_monte_carlo
from lib.capstone import render_capstone_footer

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

st.markdown(
    """
    <h1 class="hero-title" style="font-size:2.2rem;">Profile & Best Plan</h1>
    <p class="hero-sub">Set your wealth or profit target — we calculate SIP, equity split, and MF strategy, then sync every module.</p>
    """,
    unsafe_allow_html=True,
)

profile = get_profile()

# ─── Target inputs ───
st.subheader("🎯 Your targets")
t1, t2 = st.columns(2)
with t1:
    target_mode = st.radio(
        "What are you planning for?",
        ["wealth", "profit"],
        format_func=lambda x: "Target corpus (₹)" if x == "wealth" else "Target annual profit from investments (₹)",
        index=0 if profile.get("profile_target_mode", "wealth") == "wealth" else 1,
        horizontal=True,
    )
    st.session_state.profile_target_mode = target_mode

with t2:
    st.session_state.profile_target_years = st.slider(
        "Years to reach target",
        3,
        40,
        int(profile.get("profile_target_years", 15)),
    )

c1, c2, c3 = st.columns(3)
with c1:
    if target_mode == "wealth":
        st.session_state.profile_wealth_target = st.number_input(
            "Target corpus (₹)",
            100_000,
            100_000_000,
            int(profile.get("profile_wealth_target", 5_000_000)),
            step=100_000,
        )
        st.session_state.profile_profit_target = float(profile.get("profile_profit_target", 0))
    else:
        st.session_state.profile_profit_target = st.number_input(
            "Target annual profit (₹)",
            10_000,
            10_000_000,
            int(profile.get("profile_profit_target", 600_000)),
            step=50_000,
            help="Expected yearly income/gains from your portfolio at maturity.",
        )
        st.session_state.profile_wealth_target = 0

with c2:
    st.session_state.profile_risk = st.selectbox(
        "Risk tolerance",
        ["auto", "conservative", "moderate", "aggressive"],
        index=["auto", "conservative", "moderate", "aggressive"].index(
            profile.get("profile_risk", "auto")
        ),
        format_func=lambda x: x.title() if x != "auto" else "Auto (from age)",
    )

with c3:
    st.session_state.profile_expected_return = st.slider(
        "Expected return % (planning)",
        6.0,
        15.0,
        float(profile.get("profile_expected_return", 12.0)),
        0.5,
    )

st.markdown("---")
st.subheader("👤 Financial profile")
p1, p2, p3 = st.columns(3)
with p1:
    st.session_state.profile_age = st.number_input("Age", 18, 75, int(profile["profile_age"]))
    st.session_state.profile_income = st.number_input(
        "Monthly income (₹)", 0, 5_000_000, int(profile["profile_income"]), step=5000
    )
with p2:
    st.session_state.profile_sip = st.number_input(
        "Current monthly SIP (₹)", 0, 500_000, int(profile["profile_sip"]), step=1000
    )
    st.session_state.profile_equity = st.slider(
        "Current equity %", 0, 100, int(profile["profile_equity"])
    )
with p3:
    st.session_state.profile_mf_value = st.number_input(
        "MF holdings (₹)", 0, 50_000_000, int(profile["profile_mf_value"]), step=10000
    )
    st.session_state.profile_crypto_usd = st.number_input(
        "Crypto ($)", 0.0, 1_000_000.0, float(profile["profile_crypto_usd"]), step=50.0
    )

b1, b2 = st.columns(2)
with b1:
    st.session_state.profile_emergency_fund = st.checkbox(
        "Emergency fund ready", profile["profile_emergency_fund"]
    )
with b2:
    st.session_state.profile_insurance = st.checkbox(
        "Insurance in place", profile["profile_insurance"]
    )

profile = get_profile()
plan = build_best_plan(profile)

st.markdown("---")
st.subheader("✨ Recommended best plan")

st.success(plan.summary)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Required SIP", f"₹{plan.required_monthly_sip:,.0f}")
m2.metric("Recommended SIP", f"₹{plan.recommended_sip:,.0f}")
m3.metric("Equity %", f"{plan.equity_pct}%")
m4.metric("Success odds", f"{plan.success_probability * 100:.0f}%")
m5.metric("Plan grade", plan.plan_grade.split("—")[0].strip())

if plan.gap_monthly > 0:
    st.warning(f"You are ₹{plan.gap_monthly:,.0f}/month below the SIP needed for your target.")

col_plan, col_chart = st.columns([1, 1.2])

with col_plan:
    st.markdown("#### Allocation split")
    alloc_df = pd.DataFrame(
        [
            {"Bucket": "Mutual funds", "SIP (₹/mo)": plan.mf_sip, "Share %": plan.mf_pct},
            {"Bucket": "Crypto (satellite)", "SIP (₹/mo)": plan.crypto_sip, "Share %": plan.crypto_pct},
            {"Bucket": "Liquid / safety", "SIP (₹/mo)": plan.liquid_sip, "Share %": plan.liquid_pct},
        ]
    )
    st.dataframe(alloc_df, use_container_width=True, hide_index=True)

    st.markdown("#### MF planner settings")
    st.info(
        f"**Risk:** {plan.risk_profile.title()} · **Equity:** {plan.equity_pct}% · "
        f"**Strategy:** {plan.equity_strategy.replace('_', ' ').title()}"
    )

    st.markdown("#### Action checklist")
    for i, act in enumerate(plan.actions, 1):
        st.markdown(f"{i}. {act}")

with col_chart:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["MF SIP", "Crypto SIP", "Liquid SIP"],
                values=[plan.mf_sip, plan.crypto_sip, plan.liquid_sip],
                hole=0.5,
                marker=dict(colors=["#00d4aa", "#8b5cf6", "#4facfe"]),
            )
        ]
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        title="Monthly SIP split",
    )
    st.plotly_chart(fig, use_container_width=True)

    sim = run_monte_carlo(
        plan.recommended_sip,
        plan.current_wealth,
        plan.target_years,
        mean_return=profile["profile_expected_return"] / 100,
    )
    years_x = [m / 12 for m in sim["months"]]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=years_x, y=sim["p50"], line=dict(color="#00d4aa", width=3), name="Median path"))
    fig2.add_hline(y=plan.wealth_target, line_dash="dash", line_color="#fbbf24", annotation_text="Target")
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        title="Path to your target",
        xaxis_title="Years",
        yaxis_title="₹",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
if st.button("🚀 Apply this plan across the entire app", type="primary", use_container_width=True):
    apply_plan_to_session(plan)
    st.balloons()
    st.success(
        "Synced: SIP, equity %, Goal Planner primary goal, AI Advisor, Command Center & Portfolio Pulse."
    )
    st.rerun()

existing = get_recommended_plan(get_profile())
if existing and st.session_state.get("plan_applied"):
    st.caption("✅ Last applied plan is active — change targets above and re-apply to update all modules.")

health = compute_health_score(
    age=profile["profile_age"],
    monthly_income=profile["profile_income"],
    monthly_investment=plan.recommended_sip,
    has_emergency_fund=profile["profile_emergency_fund"],
    has_insurance=profile["profile_insurance"],
    equity_pct=plan.equity_pct,
)
st.markdown("---")
h1, h2 = st.columns(2)
h1.metric("Health score (with recommended SIP)", f"{health.score}/100")
h2.metric("Expected annual profit at horizon", f"₹{plan.expected_annual_profit:,.0f}")

render_capstone_footer()
