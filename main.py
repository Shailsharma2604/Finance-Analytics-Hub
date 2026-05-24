"""
Finance Analytics Hub — Final Year Project
Run: streamlit run main.py
"""

import streamlit as st
from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar
from lib.project_meta import PROJECT, MODULES
from lib.capstone import render_capstone_footer, render_tech_badges, render_demo_banner
from lib.demo_data import load_demo_into_session

st.set_page_config(
    page_title=f"{PROJECT['title']} | FYP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()
render_demo_banner()

<<<<<<< HEAD
# ─── Hero ───
st.markdown(
    f"""
    <div class="hero-animate" style="text-align:center;padding:2.5rem 1rem 1rem;">
        <span class="capstone-ribbon">🎓 {PROJECT['batch']} · {PROJECT['academic_year']}</span>
        <h1 class="hero-title">{PROJECT['title']}</h1>
        <p class="hero-sub" style="margin:1rem auto 0.5rem;max-width:720px;">
            {PROJECT['subtitle']}
        </p>
        <p style="color:#64748b;font-size:0.95rem;margin-top:1rem;">
            by <strong style="color:#00d4aa;">{PROJECT['student_name']}</strong>
            · {PROJECT['department']} · {PROJECT['institution']}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTA row
b1, b2, b3 = st.columns([1, 1, 1])
with b1:
    if st.button("🎬 Start demo walkthrough", use_container_width=True, type="primary"):
        load_demo_into_session()
        st.balloons()
        st.rerun()
with b2:
    if st.button("📋 Project overview", use_container_width=True):
        st.switch_page("pages/0_🎓_Project_Overview.py")
with b3:
    if st.button("🧠 Open AI Advisor", use_container_width=True):
        st.switch_page("pages/6_🧠_AI_Advisor.py")

st.markdown("---")

# Stats
s1, s2, s3, s4, s5 = st.columns(5)
stats = [
    ("7", "Integrated modules"),
    ("Live", "Market data"),
    ("500+", "MC simulations"),
    ("5", "Health pillars"),
    ("100", "Health score max"),
]
for col, (num, lbl) in zip([s1, s2, s3, s4, s5], stats):
    col.markdown(
        f'<div class="stat-box"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
render_tech_badges()

# Module showcase
st.markdown("### 🚀 Explore the platform")
cols = st.columns(3)
for i, (name, desc) in enumerate(MODULES):
    with cols[i % 3]:
        icons = ["🏠", "📈", "₿", "🎯", "🧠", "💓"]
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:120px;">
                <span style="font-size:1.5rem;">{icons[i]}</span>
                <strong style="display:block;color:#f1f5f9;margin:0.5rem 0;">{name}</strong>
                <small style="color:#94a3b8;">{desc}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# Why it matters — viva talking points
st.markdown(
    """
    <div class="thesis-card">
        <h3 style="color:#f1f5f9;margin-top:0;">💡 Why this project stands out</h3>
        <ul style="color:#cbd5e1;line-height:1.8;">
            <li><strong>Unified</strong> — MF + crypto + goals in one app (not scattered spreadsheets)</li>
            <li><strong>Data-driven</strong> — real Binance & Nifty/Sensex feeds, not static mockups</li>
            <li><strong>Quantitative</strong> — Monte Carlo engine with percentile bands</li>
            <li><strong>Explainable</strong> — rule-based AI advisor with prioritized actions</li>
            <li><strong>Production-style</strong> — modular codebase, session sync, HTML exports</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "👈 **Sidebar navigation** — start with **Project Overview** for viva, then **Command Center** with demo profile."
)

render_capstone_footer()
=======
# Header
st.markdown("# 💰 Finance Analytics Hub")
st.markdown("<p class='subtitle'>Choose your financial analysis tool</p>", unsafe_allow_html=True)

# Project paths
MUTUAL_FUND_APP_PATH = "https://proejct-7-1.streamlit.app/"
CRYPTO_ANALYSIS_APP_PATH = r"example-app-crypto-dashboard-main/app.py"

# Create two columns for the project cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div class='project-card'>
            <div class='project-title'>📈 Mutual Fund Analyzer</div>
            <div class='project-desc'>
                Comprehensive mutual fund portfolio planning and analysis tool
            </div>
            <ul class='feature-list'>
                <li class='feature-item'>Portfolio Allocation Optimizer</li>
                <li class='feature-item'>Risk Assessment Tools</li>
                <li class='feature-item'>Performance Analytics</li>
                <li class='feature-item'>Investment Recommendations</li>
                <li class='feature-item'>Historical Data Analysis</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Mutual Fund Analyzer", key="mutual_fund"):
        if os.path.exists(MUTUAL_FUND_APP_PATH):
            st.success("✅ Launching Mutual Fund Analyzer...")
            st.balloons()
            subprocess.Popen(["streamlit", "run", MUTUAL_FUND_APP_PATH])
            st.info("📌 The app will open in a new browser tab")
        else:
            st.error("❌ File not found. Please check the path.")

with col2:
    st.markdown("""
        <div class='project-card'>
            <div class='project-title'>₿ Crypto Analytics Dashboard</div>
            <div class='project-desc'>
                Advanced cryptocurrency market analysis and insights platform
            </div>
            <ul class='feature-list'>
                <li class='feature-item'>Real-time Price Tracking</li>
                <li class='feature-item'>Market Trend Analysis</li>
                <li class='feature-item'>Technical Indicators</li>
                <li class='feature-item'>Portfolio Monitoring</li>
                <li class='feature-item'>Multi-Currency Support</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Crypto Analytics", key="crypto"):
        if os.path.exists(CRYPTO_ANALYSIS_APP_PATH):
            st.success("✅ Launching Crypto Analytics Dashboard...")
            st.balloons()
            subprocess.Popen(["streamlit", "run", CRYPTO_ANALYSIS_APP_PATH])
            st.info("📌 The app will open in a new browser tab")
        else:
            st.error("❌ File not found. Please check the path.")

# Footer
st.markdown("---")
st.markdown(f"""
    <div class='footer'>
        <p>🕐 Current Time: {datetime.now().strftime('%B %d, %Y - %I:%M %p')}</p>
        <p>💡 Tip: Each project runs independently in a separate browser tab</p>
        <p>⚡ Built with Streamlit | Finance Analytics Hub</p>
    </div>
""", unsafe_allow_html=True)
>>>>>>> 480f4809ccf98aa5c66210c9b48bed8ad5717658
