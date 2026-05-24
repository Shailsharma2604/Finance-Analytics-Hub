"""Final Year Project — overview, architecture, objectives (viva-ready)."""

import streamlit as st
from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar
from lib.project_meta import PROJECT, OBJECTIVES, TECH_STACK, MODULES
from lib.capstone import render_capstone_footer, render_tech_badges
from lib.demo_data import load_demo_into_session

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

st.markdown(
    f"""
    <div class="hero-animate" style="text-align:center;padding:1rem 0 2rem;">
        <span class="capstone-ribbon">🎓 Final Year Project · {PROJECT['academic_year']}</span>
        <h1 class="hero-title">{PROJECT['title']}</h1>
        <p class="hero-sub" style="margin:0.75rem auto;">{PROJECT['subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Student info card
st.markdown(
    f"""
    <div class="thesis-card">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.5rem;">
            <div><p style="color:#64748b;margin:0;font-size:0.8rem;">Submitted by</p>
            <p style="color:#f1f5f9;font-size:1.1rem;font-weight:700;margin:0.25rem 0;">{PROJECT['student_name']}</p>
            <p style="color:#94a3b8;margin:0;">{PROJECT['roll_number']}</p></div>
            <div><p style="color:#64748b;margin:0;font-size:0.8rem;">Department</p>
            <p style="color:#f1f5f9;font-weight:600;margin:0.25rem 0;">{PROJECT['department']}</p>
            <p style="color:#94a3b8;margin:0;">{PROJECT['batch']}</p></div>
            <div><p style="color:#64748b;margin:0;font-size:0.8rem;">Institution</p>
            <p style="color:#f1f5f9;font-weight:600;margin:0.25rem 0;">{PROJECT['institution']}</p></div>
            <div><p style="color:#64748b;margin:0;font-size:0.8rem;">Guide</p>
            <p style="color:#f1f5f9;font-weight:600;margin:0.25rem 0;">{PROJECT['guide_name']}</p></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("🎬 Load demo profile for presentation", use_container_width=True, type="primary"):
        load_demo_into_session()
        st.balloons()
        st.success("Demo loaded! Open **AI Advisor** or **Command Center** next.")
with c2:
    st.caption("Use demo mode during viva — realistic student profile pre-filled.")

tab1, tab2, tab3, tab4 = st.tabs(["📋 Abstract", "🏗️ Architecture", "🛠️ Tech Stack", "🔮 Future Scope"])

with tab1:
    st.markdown("### Problem Statement")
    st.markdown(
        """
        Retail investors in India juggle **mutual funds**, **crypto**, and **multiple goals** (house, education, retirement)
        across disconnected tools. Most apps either focus on trading or generic calculators — not unified,
        data-driven planning with live markets and explainable recommendations.
        """
    )
    st.markdown("### Objectives")
    for i, obj in enumerate(OBJECTIVES, 1):
        st.markdown(f'<div class="objective-item"><strong>O{i}.</strong> {obj}</div>', unsafe_allow_html=True)

    st.markdown("### Methodology")
    st.markdown(
        """
        1. **Requirements** — survey of investor needs (allocation, goals, crypto exposure)  
        2. **Design** — modular Streamlit architecture with shared session state  
        3. **Implementation** — Python engines for allocation, Monte Carlo, health scoring  
        4. **Integration** — Binance + Yahoo Finance APIs for live data  
        5. **Validation** — scenario testing with demo profiles and edge cases  
        """
    )

with tab2:
    st.markdown("### System Architecture")
    st.code(
        """
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI LAYER                        │
│  Overview │ Command │ MF │ Crypto │ Goals │ AI │ Pulse    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     SHARED LIB (lib/)                        │
│  session │ health_score │ simulator │ goals │ insights     │
│  market_data │ india_markets │ market_mood │ report          │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Allocation    │  │ Binance API   │  │ Yahoo Finance │
│ Engine (MF)   │  │ Crypto data   │  │ Nifty/Sensex  │
└───────────────┘  └───────────────┘  └───────────────┘
        """,
        language=None,
    )
    st.markdown("### Module Map")
    for name, desc in MODULES:
        st.markdown(f"- **{name}** — {desc}")

with tab3:
    render_tech_badges()
    st.markdown("| Technology | Role |")
    st.markdown("|------------|------|")
    for name, role in TECH_STACK:
        st.markdown(f"| **{name}** | {role} |")

with tab4:
    st.markdown(
        """
        - **ML-based risk profiling** — train on historical volatility clusters  
        - **NSE stock screener** — extend beyond crypto to Indian equities  
        - **User authentication** — save portfolios with Firebase / PostgreSQL  
        - **Mobile app** — React Native wrapper for on-the-go tracking  
        - **SEBI-compliant disclaimers** — integrate regulated advisory workflows  
        """
    )

st.markdown("---")
st.markdown("### 📊 Project Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.markdown('<div class="stat-box"><div class="num">7</div><div class="lbl">Modules</div></div>', unsafe_allow_html=True)
m2.markdown('<div class="stat-box"><div class="num">15+</div><div class="lbl">Python modules</div></div>', unsafe_allow_html=True)
m3.markdown('<div class="stat-box"><div class="num">2</div><div class="lbl">Live APIs</div></div>', unsafe_allow_html=True)
m4.markdown('<div class="stat-box"><div class="num">500</div><div class="lbl">MC simulations</div></div>', unsafe_allow_html=True)

render_capstone_footer()
