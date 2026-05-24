"""Premium fintech UI theme — glassmorphism, dark mode, motion."""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-deep: #0a0e17;
    --bg-card: rgba(255, 255, 255, 0.04);
    --bg-glass: rgba(255, 255, 255, 0.06);
    --border-glass: rgba(255, 255, 255, 0.1);
    --accent-cyan: #00d4aa;
    --accent-purple: #8b5cf6;
    --accent-gold: #fbbf24;
    --accent-rose: #f43f5e;
    --text-primary: #f1f5f9;
    --text-muted: #94a3b8;
    --glow-cyan: 0 0 40px rgba(0, 212, 170, 0.25);
    --glow-purple: 0 0 40px rgba(139, 92, 246, 0.2);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background: var(--bg-deep) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139, 92, 246, 0.18), transparent),
        radial-gradient(ellipse 60% 40% at 100% 50%, rgba(0, 212, 170, 0.08), transparent),
        radial-gradient(ellipse 50% 30% at 0% 80%, rgba(251, 191, 36, 0.06), transparent) !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 1400px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 14, 23, 0.95) !important;
    border-right: 1px solid var(--border-glass) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--glow-cyan);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--glow-purple);
}
div[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 100%) !important;
    color: #0a0e17 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: var(--glow-cyan);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: var(--bg-glass);
    border-radius: 14px;
    padding: 0.35rem;
    border: 1px solid var(--border-glass);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: var(--text-muted);
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,212,170,0.2), rgba(139,92,246,0.2)) !important;
    color: var(--accent-cyan) !important;
}

/* Dataframes */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-glass);
}

/* Custom components */
.hero-title {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, var(--accent-cyan) 50%, var(--accent-purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    line-height: 1.15;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 1.15rem;
    max-width: 640px;
    line-height: 1.6;
}
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.glass-card:hover {
    border-color: rgba(0, 212, 170, 0.35);
    box-shadow: var(--glow-cyan);
}
.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--accent-cyan);
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0, 212, 170, 0.6); }
    50% { opacity: 0.8; box-shadow: 0 0 0 8px rgba(0, 212, 170, 0); }
}
.score-ring {
    font-size: 3.5rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.badge-live {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    background: rgba(0, 212, 170, 0.15);
    border: 1px solid rgba(0, 212, 170, 0.4);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.ticker-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border-glass);
}
.ticker-item:last-child { border-bottom: none; }
.ticker-symbol { font-weight: 600; color: var(--text-primary); }
.ticker-price { font-family: 'JetBrains Mono', monospace; color: var(--text-primary); }
.ticker-change-up { color: #34d399; font-size: 0.9rem; }
.ticker-change-down { color: var(--accent-rose); font-size: 0.9rem; }
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}
.feature-chip {
    background: var(--bg-card);
    border: 1px solid var(--border-glass);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    text-align: center;
}
.feature-chip span { font-size: 1.75rem; display: block; margin-bottom: 0.5rem; }
.feature-chip strong { color: var(--text-primary); display: block; margin-bottom: 0.25rem; }
.feature-chip small { color: var(--text-muted); font-size: 0.85rem; }
.mood-bar {
    height: 12px;
    border-radius: 999px;
    background: linear-gradient(90deg, #f43f5e 0%, #fbbf24 50%, #00d4aa 100%);
    position: relative;
    margin: 1rem 0;
}
.mood-marker {
    position: absolute;
    top: -4px;
    width: 4px;
    height: 20px;
    background: white;
    border-radius: 2px;
    box-shadow: 0 0 12px white;
    transform: translateX(-50%);
}
.sidebar-brand {
    text-align: center;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid var(--border-glass);
    margin-bottom: 1rem;
}
.sidebar-brand h2 {
    font-size: 1.1rem !important;
    margin: 0.5rem 0 0 !important;
    background: linear-gradient(135deg, #00d4aa, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.capstone-ribbon {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,212,170,0.2), rgba(139,92,246,0.2));
    border: 1px solid rgba(0,212,170,0.4);
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #00d4aa;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.thesis-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.thesis-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4aa, #8b5cf6, #fbbf24);
}
.stat-box {
    text-align: center;
    padding: 1.25rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
}
.stat-box .num {
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #00d4aa, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-box .lbl { color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem; }
.tech-badge {
    display: inline-block;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.35);
    color: #c4b5fd;
    padding: 0.35rem 0.85rem;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.2rem;
}
.objective-item {
    padding: 0.75rem 0 0.75rem 1.5rem;
    border-left: 3px solid #00d4aa;
    margin: 0.5rem 0;
    color: #cbd5e1;
    line-height: 1.5;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
.hero-animate { animation: fadeUp 0.8s ease-out; }
</style>
"""


def inject_theme():
    import streamlit as st

    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_sidebar_brand():
    import streamlit as st
    from lib.project_meta import PROJECT

    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <span style="font-size:2rem;">🎓</span>
            <h2>{PROJECT['title']}</h2>
            <p style="color:#00d4aa;font-size:0.7rem;margin:0.25rem 0;font-weight:600;">
                Final Year Project · {PROJECT['academic_year']}
            </p>
            <p style="color:#64748b;font-size:0.7rem;margin:0;">{PROJECT['student_name']} · {PROJECT['roll_number']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
