"""Crypto Intelligence — live prices, charts, movers, portfolio tracker."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar
from lib.market_data import (
    fetch_ticker_24h_with_source,
    fetch_klines,
    format_price,
    top_movers,
    CRYPTO_OPTIONS,
    get_symbol_row,
    data_source_banner,
)

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

st.markdown(
    """
    <p class="badge-live"><span class="pulse-dot"></span> Binance live</p>
    <h1 class="hero-title" style="font-size:2.2rem;">Crypto Intelligence</h1>
    <p class="hero-sub">Real-time prices, interactive charts, market movers, and your personal watchlist.</p>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=60)
def load_data():
    return fetch_ticker_24h_with_source()


if st.sidebar.button("🔄 Refresh now"):
    load_data.clear()
    st.rerun()
st.sidebar.caption("Prices cache for 60 seconds")


try:
    df, data_source = load_data()
except Exception as e:
    st.error(f"Could not load crypto market data: {e}")
    st.stop()

banner = data_source_banner(data_source)
if banner:
    st.info(banner)

# --- Top metrics row ---
selected_label = st.sidebar.selectbox("Chart asset", list(CRYPTO_OPTIONS.keys()), index=0)
symbol = CRYPTO_OPTIONS[selected_label]
row = get_symbol_row(df, symbol)

if row is not None:
    price = float(row["lastPrice"])
    pct = float(row["priceChangePercent"])
    high = float(row["highPrice"])
    low = float(row["lowPrice"])
    vol = float(row["quoteVolume"])

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(selected_label.split()[0], format_price(price), f"{pct:+.2f}%")
    c2.metric("24h High", format_price(high))
    c3.metric("24h Low", format_price(low))
    c4.metric("24h Volume", f"${vol/1e6:.1f}M")
    c5.metric("Symbol", symbol)

# --- Tabs ---
tab_chart, tab_movers, tab_watch, tab_all = st.tabs(
    ["📊 Price Chart", "🔥 Movers", "⭐ My Watchlist", "📋 All Markets"]
)

with tab_chart:
    interval = st.radio("Interval", ["1h", "4h", "1d"], horizontal=True, key="interval")
    limit = {"1h": 168, "4h": 120, "1d": 90}[interval]

    try:
        klines = fetch_klines(symbol, interval=interval, limit=limit)
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
        )
        fig.add_trace(
            go.Candlestick(
                x=klines["open_time"],
                open=klines["open"],
                high=klines["high"],
                low=klines["low"],
                close=klines["close"],
                increasing_line_color="#00d4aa",
                decreasing_line_color="#f43f5e",
                name="OHLC",
            ),
            row=1,
            col=1,
        )
        colors = [
            "#00d4aa" if c >= o else "#f43f5e"
            for c, o in zip(klines["close"], klines["open"])
        ]
        fig.add_trace(
            go.Bar(x=klines["open_time"], y=klines["volume"], marker_color=colors, opacity=0.5, name="Volume"),
            row=2,
            col=1,
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=520,
            margin=dict(t=40, b=40, l=50, r=20),
            xaxis_rangeslider_visible=False,
            showlegend=False,
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Chart unavailable: {e}")

with tab_movers:
    gainers, losers = top_movers(df, n=8)
    gc, lc = st.columns(2)
    with gc:
        st.subheader("🟢 Top Gainers")
        g = gainers.copy()
        g["lastPrice"] = g["lastPrice"].apply(lambda x: format_price(float(x)))
        g["priceChangePercent"] = g["priceChangePercent"].apply(lambda x: f"+{float(x):.2f}%")
        g.columns = ["Symbol", "Price", "Change", "Volume (USDT)"]
        st.dataframe(g, use_container_width=True, hide_index=True)
    with lc:
        st.subheader("🔴 Top Losers")
        l = losers.copy()
        l["lastPrice"] = l["lastPrice"].apply(lambda x: format_price(float(x)))
        l["priceChangePercent"] = l["priceChangePercent"].apply(lambda x: f"{float(x):.2f}%")
        l.columns = ["Symbol", "Price", "Change", "Volume (USDT)"]
        st.dataframe(l, use_container_width=True, hide_index=True)

with tab_watch:
    st.caption("Build your watchlist — prices update on refresh")
    picks = st.multiselect(
        "Assets",
        list(CRYPTO_OPTIONS.keys()),
        default=list(CRYPTO_OPTIONS.keys())[:6],
    )
    wcols = st.columns(min(len(picks), 4) or 1)
    for i, label in enumerate(picks):
        sym = CRYPTO_OPTIONS[label]
        r = get_symbol_row(df, sym)
        if r is None:
            continue
        with wcols[i % len(wcols)]:
            st.metric(
                label.split("(")[0].strip(),
                format_price(float(r["lastPrice"])),
                f"{float(r['priceChangePercent']):+.2f}%",
            )

    # Simple portfolio tracker
    st.markdown("---")
    st.subheader("💼 Paper Portfolio")
    with st.expander("Track holdings (demo)", expanded=False):
        holdings = st.data_editor(
            pd.DataFrame(
                {"Asset": ["Bitcoin (BTC)", "Ethereum (ETH)"], "Units": [0.05, 1.2], "Avg Buy ($)": [42000, 2200]}
            ),
            num_rows="dynamic",
            use_container_width=True,
        )
        total_val = 0.0
        for _, h in holdings.iterrows():
            sym = CRYPTO_OPTIONS.get(h["Asset"])
            if not sym:
                continue
            r = get_symbol_row(df, sym)
            if r is not None:
                total_val += float(h["Units"]) * float(r["lastPrice"])
        st.metric("Portfolio value (live)", f"${total_val:,.2f}")

with tab_all:
    usdt = df[df["symbol"].str.endswith("USDT")].copy()
    usdt["lastPrice"] = usdt["lastPrice"].astype(float)
    usdt["priceChangePercent"] = usdt["priceChangePercent"].astype(float)
    usdt["quoteVolume"] = usdt["quoteVolume"].astype(float)
    usdt = usdt.nlargest(50, "quoteVolume")[
        ["symbol", "lastPrice", "priceChangePercent", "highPrice", "lowPrice", "quoteVolume"]
    ]
    usdt.columns = ["Symbol", "Price", "Change %", "High", "Low", "Volume"]
    st.dataframe(usdt, use_container_width=True, height=500)
    st.download_button(
        "📥 Download CSV",
        usdt.to_csv(index=False).encode(),
        "crypto_markets.csv",
        "text/csv",
    )
