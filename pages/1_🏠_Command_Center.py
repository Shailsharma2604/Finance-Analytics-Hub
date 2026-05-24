"""Command Center — live markets, India indices, mood, Monte Carlo."""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.capstone import render_demo_banner
from lib.market_data import fetch_ticker_24h, watchlist_snapshot, format_price
from lib.health_score import compute_health_score
from lib.market_mood import compute_market_mood
from lib.india_markets import fetch_india_indices, format_inr
from lib.simulator import run_monte_carlo

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()
render_demo_banner()

profile = get_profile()

st.markdown(
    """
    <p class="badge-live"><span class="pulse-dot"></span> Markets live</p>
    <h1 class="hero-title">Command Center</h1>
    <p class="hero-sub">India indices · crypto mood · health score · Monte Carlo wealth engine.</p>
    """,
    unsafe_allow_html=True,
)

# --- India indices ---
st.subheader("🇮🇳 Indian Markets")
try:
    indices = fetch_india_indices()
    if indices:
        icols = st.columns(len(indices))
        for i, idx in enumerate(indices):
            with icols[i]:
                st.metric(
                    idx["name"],
                    format_inr(idx["price"]),
                    f"{idx['change_pct']:+.2f}%",
                    delta_color="normal" if idx["change_pct"] >= 0 else "inverse",
                )
    else:
        st.caption("Indian indices unavailable — check network")
except Exception as e:
    st.caption(f"Indices: {e}")

st.markdown("---")

@st.cache_data(ttl=60)
def load_markets():
    return fetch_ticker_24h()


try:
    with st.spinner("Syncing markets…"):
        ticker_df = load_markets()
    watchlist = watchlist_snapshot(ticker_df)
    mood = compute_market_mood(ticker_df)

    # Crypto top row
    cols = st.columns(5)
    for i, item in enumerate(watchlist[:5]):
        with cols[i]:
            st.metric(item["label"], format_price(item["price"]), f"{item['change_pct']:+.2f}%")

    # Mood gauge
    st.subheader("🌡️ Crypto Market Mood")
    marker_left = mood["score"]
    st.markdown(
        f"""
        <div class="glass-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:2rem;font-weight:800;color:{mood['color']};">{mood['score']}</span>
                <span style="font-weight:700;color:{mood['color']};">{mood['label']}</span>
            </div>
            <div class="mood-bar"><div class="mood-marker" style="left:{marker_left}%;"></div></div>
            <p style="color:#94a3b8;font-size:0.85rem;margin:0;">
                Rising pairs: {mood['details'].get('pairs_rising','—')} ·
                Avg change: {mood['details'].get('avg_change','—')} ·
                BTC: {mood['details'].get('btc_24h','—')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("📡 Crypto Watchlist")
        st.caption(f"Updated {datetime.now().strftime('%H:%M:%S')}")
        for item in watchlist:
            chg_class = "ticker-change-up" if item["change_pct"] >= 0 else "ticker-change-down"
            arrow = "▲" if item["change_pct"] >= 0 else "▼"
            st.markdown(
                f"""<div class="ticker-item">
                <span class="ticker-symbol">{item['label']}</span>
                <span><span class="ticker-price">{format_price(item['price'])}</span>
                <span class="{chg_class}"> {arrow} {item['change_pct']:+.2f}%</span></span></div>""",
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("🧮 Health Score")
        health = compute_health_score(
            age=profile["profile_age"],
            monthly_income=profile["profile_income"],
            monthly_investment=profile["profile_sip"],
            has_emergency_fund=profile["profile_emergency_fund"],
            has_insurance=profile["profile_insurance"],
            equity_pct=profile["profile_equity"],
        )
        st.markdown(
            f"""<div class="glass-card" style="text-align:center;">
            <div class="score-ring">{health.score}</div>
            <p style="color:{health.color};font-weight:700;">{health.grade}</p></div>""",
            unsafe_allow_html=True,
        )
        for pillar, pts in health.breakdown.items():
            st.progress(pts / 20, text=f"{pillar}: {pts}/20")

except Exception as e:
    st.warning(f"Market data unavailable: {e}")

# --- Monte Carlo ---
st.markdown("---")
st.subheader("🔮 Monte Carlo Wealth Simulator")
st.caption("500 simulated paths — see best, median, and worst-case outcomes")

mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    mc_sip = st.number_input("Monthly SIP (₹)", 1000, 500_000, int(profile["profile_sip"]), step=5000, key="mc_sip")
with mc2:
    mc_lump = st.number_input("Lumpsum (₹)", 0, 10_000_000, 0, step=50000, key="mc_lump")
with mc3:
    mc_years = st.slider("Years", 5, 35, 20, key="mc_years")
with mc4:
    mc_vol = st.slider("Volatility %", 8.0, 35.0, 18.0, key="mc_vol")

mc_ret = st.slider("Expected return %", 6.0, 16.0, 12.0, 0.5, key="mc_ret")

sim = run_monte_carlo(mc_sip, mc_lump, mc_years, mean_return=mc_ret / 100, volatility=mc_vol / 100)
years_x = [m / 12 for m in sim["months"]]

fig_mc = go.Figure()
fig_mc.add_trace(go.Scatter(x=years_x, y=sim["p90"], line=dict(width=0), showlegend=False))
fig_mc.add_trace(
    go.Scatter(
        x=years_x, y=sim["p10"], fill="tonexty",
        fillcolor="rgba(139,92,246,0.25)", line=dict(width=0), name="10th–90th %ile",
    )
)
fig_mc.add_trace(go.Scatter(x=years_x, y=sim["p50"], line=dict(color="#00d4aa", width=3), name="Median"))
fig_mc.add_trace(
    go.Scatter(
        x=years_x, y=[mc_sip * 12 * y + mc_lump for y in years_x],
        line=dict(color="#64748b", dash="dot", width=2), name="Invested",
    )
)
fig_mc.update_layout(
    template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=400,
    xaxis_title="Years", yaxis_title="₹", legend=dict(orientation="h", y=1.08),
)
st.plotly_chart(fig_mc, use_container_width=True)

r1, r2, r3, r4 = st.columns(4)
r1.metric("Median", f"₹{sim['final_median']:,.0f}")
r2.metric("Bear case (10%)", f"₹{sim['final_p10']:,.0f}")
r3.metric("Bull case (90%)", f"₹{sim['final_p90']:,.0f}")
r4.metric("Invested", f"₹{sim['total_invested']:,.0f}")

# Deterministic comparison
st.markdown("---")
st.subheader("📊 Deterministic Projection")
pc1, pc2 = st.columns(2)
with pc1:
    proj_years = st.slider("Years", 5, 30, 10, key="det_years")
with pc2:
    proj_ret = st.slider("Fixed return %", 6.0, 15.0, 12.0, 0.5, key="det_ret")

months = proj_years * 12
r = proj_ret / 12 / 100
fv = mc_sip * (((1 + r) ** months - 1) / r) * (1 + r) + mc_lump * ((1 + r) ** months) if r else mc_sip * months + mc_lump
st.metric(f"{proj_years}-year corpus (fixed {proj_ret}%)", f"₹{fv:,.0f}")
