"""Portfolio Pulse — unified snapshot with HTML report export."""

import streamlit as st
import plotly.graph_objects as go

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.market_data import fetch_ticker_24h, watchlist_snapshot, format_price
from lib.health_score import compute_health_score
from lib.market_mood import compute_market_mood
from lib.report import build_html_report

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

profile = get_profile()

st.markdown(
    """
    <h1 class="hero-title" style="font-size:2.2rem;">Portfolio Pulse</h1>
    <p class="hero-sub">Unified view — synced from your global profile in the sidebar.</p>
    """,
    unsafe_allow_html=True,
)

age = profile["profile_age"]
income = profile["profile_income"]
sip = profile["profile_sip"]
equity = profile["profile_equity"]
mf_value = profile["profile_mf_value"]
crypto_usd = profile["profile_crypto_usd"]
usd_inr = profile["profile_usd_inr"]
ef = profile["profile_emergency_fund"]
ins = profile["profile_insurance"]

col_profile, col_market = st.columns([1, 1])

with col_profile:
    st.subheader("👤 Your Profile")
    st.caption("Edit in sidebar → applies everywhere")

    mf_value = st.number_input("MF portfolio (₹)", 0, 50_000_000, int(mf_value), step=50000, key="pulse_mf")
    crypto_usd = st.number_input("Crypto ($)", 0.0, 1_000_000.0, float(crypto_usd), step=100.0, key="pulse_crypto")
    usd_inr = st.number_input("USD→INR", 70.0, 100.0, float(usd_inr), 0.5, key="pulse_inr")
    st.session_state.profile_mf_value = mf_value
    st.session_state.profile_crypto_usd = crypto_usd
    st.session_state.profile_usd_inr = usd_inr

    health = compute_health_score(
        age=age, monthly_income=income, monthly_investment=sip,
        has_emergency_fund=ef, has_insurance=ins, equity_pct=equity,
    )
    st.markdown(
        f"""<div class="glass-card" style="text-align:center;">
        <div class="score-ring">{health.score}</div>
        <p style="color:{health.color};font-weight:700;">{health.grade}</p></div>""",
        unsafe_allow_html=True,
    )

with col_market:
    st.subheader("🌐 Market Pulse")
    try:
        df = fetch_ticker_24h()
        mood = compute_market_mood(df)
        st.metric("Crypto Mood", mood["label"], f"{mood['score']}/100")
        for item in watchlist_snapshot(df)[:5]:
            st.metric(item["label"], format_price(item["price"]), f"{item['change_pct']:+.2f}%")
    except Exception:
        st.caption("Markets offline")

st.markdown("---")
st.subheader("🥧 Asset Mix")

crypto_inr = crypto_usd * usd_inr
total = mf_value + crypto_inr
if total > 0:
    mf_pct = mf_value / total * 100
    crypto_pct = crypto_inr / total * 100
    cash_pct = max(0, 100 - mf_pct - crypto_pct)

    fig = go.Figure(
        data=[go.Pie(
            labels=["Mutual Funds", "Crypto", "Other"],
            values=[mf_pct, crypto_pct, cash_pct],
            hole=0.55,
            marker=dict(colors=["#00d4aa", "#8b5cf6", "#334155"]),
        )]
    )
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=400,
        annotations=[dict(text=f"<b>₹{total:,.0f}</b><br>Total", x=0.5, y=0.5, font=dict(size=18, color="#f1f5f9"), showarrow=False)],
    )
    st.plotly_chart(fig, use_container_width=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Mutual Funds", f"₹{mf_value:,.0f}", f"{mf_pct:.1f}%")
    m2.metric("Crypto", f"₹{crypto_inr:,.0f}", f"{crypto_pct:.1f}%")
    m3.metric("Combined", f"₹{total:,.0f}")

st.markdown("---")
st.subheader("🎯 Actions")
for tip in health.insights:
    st.info(tip)

try:
    mood = compute_market_mood(fetch_ticker_24h())
except Exception:
    mood = {"label": "N/A", "score": 50}

html = build_html_report(profile, health.score, health.grade, health.insights, total, mood["label"], mood["score"])
st.download_button("📄 Download portfolio report (HTML)", html.encode(), "portfolio_report.html", "text/html", use_container_width=True)

fig_bar = go.Figure(go.Bar(
    x=list(health.breakdown.values()), y=list(health.breakdown.keys()), orientation="h",
    marker=dict(color=["#00d4aa" if v >= 14 else "#fbbf24" if v >= 8 else "#f43f5e" for v in health.breakdown.values()]),
))
fig_bar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=260, xaxis=dict(range=[0, 20]))
st.plotly_chart(fig_bar, use_container_width=True)
