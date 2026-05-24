"""AI Advisor — intelligent, prioritized financial guidance."""

import streamlit as st
import plotly.graph_objects as go

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.health_score import compute_health_score
from lib.market_data import fetch_ticker_24h
from lib.market_mood import compute_market_mood
from lib.insights import generate_advisor_insights
from lib.report import build_html_report
from lib.simulator import run_monte_carlo
from lib.capstone import render_capstone_footer, render_demo_banner
from lib.project_meta import PROJECT

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()
render_demo_banner()

st.markdown(
    f"""
    <p class="badge-live"><span class="pulse-dot"></span> Advisor online · FYP Module</p>
    <h1 class="hero-title" style="font-size:2.2rem;">AI Financial Advisor</h1>
    <p class="hero-sub">Rule-based intelligent engine — analyzes {PROJECT['student_name']}'s profile,
    goals gap, and live crypto mood to deliver prioritized actions.</p>
    """,
    unsafe_allow_html=True,
)

profile = get_profile()
health = compute_health_score(
    age=profile["profile_age"],
    monthly_income=profile["profile_income"],
    monthly_investment=profile["profile_sip"],
    has_emergency_fund=profile["profile_emergency_fund"],
    has_insurance=profile["profile_insurance"],
    equity_pct=profile["profile_equity"],
)

try:
    mood = compute_market_mood(fetch_ticker_24h())
except Exception:
    mood = {"score": 50, "label": "Neutral", "color": "#fbbf24", "details": {}}

goals_gap = st.session_state.get("goals_gap_total", 0)
insights = generate_advisor_insights(profile, mood["score"], mood["label"], goals_gap)

# Top row: health + mood gauges
g1, g2, g3 = st.columns([1, 1, 1.2])

with g1:
    st.markdown(
        f"""
        <div class="glass-card" style="text-align:center;">
            <p style="color:#94a3b8;margin:0;">Health Score</p>
            <div class="score-ring">{health.score}</div>
            <p style="color:{health.color};font-weight:700;">{health.grade}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with g2:
    st.markdown(
        f"""
        <div class="glass-card" style="text-align:center;">
            <p style="color:#94a3b8;margin:0;">Crypto Mood</p>
            <div class="score-ring" style="background:linear-gradient(135deg,{mood['color']},{mood['color']});-webkit-background-clip:text;">{mood['score']}</div>
            <p style="color:{mood['color']};font-weight:700;">{mood['label']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for k, v in mood.get("details", {}).items():
        st.caption(f"{k.replace('_',' ').title()}: {v}")

with g3:
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health.score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Overall Readiness"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": health.color},
                "steps": [
                    {"range": [0, 40], "color": "rgba(244,63,94,0.3)"},
                    {"range": [40, 70], "color": "rgba(251,191,36,0.3)"},
                    {"range": [70, 100], "color": "rgba(0,212,170,0.3)"},
                ],
            },
        )
    )
    fig_gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(t=40, b=10, l=30, r=30),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")
st.subheader("📋 Prioritized Action Plan")

for i, item in enumerate(insights[:6]):
    urgency = "🔴" if item["priority"] <= 2 else "🟡" if item["priority"] <= 5 else "🟢"
    with st.expander(f"{urgency} **{item['title']}** — {item['category']}", expanded=(i < 2)):
        st.write(item["body"])
        st.success(f"**Action:** {item['action']}")

# Monte Carlo quick insight
st.markdown("---")
st.subheader("🔮 Wealth Outlook (Monte Carlo)")
mc1, mc2, mc3 = st.columns(3)
with mc1:
    mc_years = st.selectbox("Horizon", [10, 15, 20, 25], index=1)
with mc2:
    mc_vol = st.slider("Volatility %", 10.0, 30.0, 18.0)
with mc3:
    mc_ret = st.slider("Expected return %", 8.0, 15.0, 12.0)

sim = run_monte_carlo(
    profile["profile_sip"],
    0,
    mc_years,
    mean_return=mc_ret / 100,
    volatility=mc_vol / 100,
)

fig_mc = go.Figure()
years_x = [m / 12 for m in sim["months"]]
fig_mc.add_trace(go.Scatter(x=years_x, y=sim["p90"], fill=None, line=dict(width=0), showlegend=False))
fig_mc.add_trace(
    go.Scatter(
        x=years_x,
        y=sim["p10"],
        fill="tonexty",
        fillcolor="rgba(139,92,246,0.2)",
        line=dict(width=0),
        name="10th–90th percentile",
    )
)
fig_mc.add_trace(go.Scatter(x=years_x, y=sim["p50"], line=dict(color="#00d4aa", width=3), name="Median"))
fig_mc.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    height=380,
    title=f"{mc_years}-year projection (500 simulations)",
    xaxis_title="Years",
    yaxis_title="₹",
)
st.plotly_chart(fig_mc, use_container_width=True)

c1, c2, c3 = st.columns(3)
c1.metric("Median outcome", f"₹{sim['final_median']:,.0f}")
c2.metric("Conservative (10th %)", f"₹{sim['final_p10']:,.0f}")
c3.metric("Optimistic (90th %)", f"₹{sim['final_p90']:,.0f}")

# Report export
st.markdown("---")
crypto_inr = profile["profile_crypto_usd"] * profile["profile_usd_inr"]
total = profile["profile_mf_value"] + crypto_inr
html = build_html_report(
    profile,
    health.score,
    health.grade,
    [f"{x['title']}: {x['action']}" for x in insights],
    total,
    mood["label"],
    mood["score"],
)
st.download_button(
    "📄 Download full advisor report (HTML)",
    html.encode(),
    f"FYP_Advisor_Report_{PROJECT['student_name'].replace(' ', '_')}.html",
    "text/html",
    use_container_width=True,
)

render_capstone_footer()
