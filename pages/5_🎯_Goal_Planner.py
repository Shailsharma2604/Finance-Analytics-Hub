"""Goal Planner — multi-goal SIP calculator with timeline visualization."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from lib.theme import inject_theme, render_sidebar_brand
from lib.session import init_profile, render_profile_sidebar, get_profile
from lib.goals import plan_goal, monthly_sip_for_goal, asset_for_horizon
from lib.simulator import probability_of_reaching_goal
from lib.plan_banner import render_active_plan_banner
from lib.plan_engine import get_recommended_plan

inject_theme()
init_profile()
render_sidebar_brand()
render_profile_sidebar()

st.markdown(
    """
    <h1 class="hero-title" style="font-size:2.2rem;">Goal Planner</h1>
    <p class="hero-sub">Map every dream to a number — house, retirement, education — with required SIP and asset mix.</p>
    """,
    unsafe_allow_html=True,
)

profile = get_profile()
total_sip = profile["profile_sip"]
render_active_plan_banner()
plan = get_recommended_plan(profile)

st.subheader("🎯 Your Goals")
st.caption("Edit rows below — we'll calculate required SIP and whether you're on track.")

wealth = profile.get("profile_wealth_target", 2_500_000) or 2_500_000
years = profile.get("profile_target_years", 7)
saved = int(profile["profile_mf_value"] + profile["profile_crypto_usd"] * profile["profile_usd_inr"])
sip_row = int(plan.recommended_sip) if plan else int(profile["profile_sip"])

default_goals = pd.DataFrame(
    [
        {"Goal": "Wealth target (profile)", "Target (₹)": wealth, "Years": years, "Priority": 1, "Saved (₹)": saved, "Your SIP (₹)": sip_row},
        {"Goal": "Child Education", "Target (₹)": 3_000_000, "Years": 12, "Priority": 2, "Saved (₹)": 50_000, "Your SIP (₹)": 8_000},
        {"Goal": "Retirement Corpus", "Target (₹)": 5_000_000, "Years": 25, "Priority": 3, "Saved (₹)": 300_000, "Your SIP (₹)": 12_000},
    ]
)

if "goals_df" not in st.session_state:
    st.session_state.goals_df = default_goals
elif st.session_state.get("plan_applied") and plan:
    st.caption("Primary goal synced from your Profile & Plan target.")

edited = st.data_editor(
    st.session_state.goals_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Target (₹)": st.column_config.NumberColumn(min_value=10000, step=50000, format="%d"),
        "Years": st.column_config.NumberColumn(min_value=1, max_value=40),
        "Priority": st.column_config.NumberColumn(min_value=1, max_value=5),
        "Your SIP (₹)": st.column_config.NumberColumn(min_value=0, step=1000),
    },
    key="goals_editor",
)
st.session_state.goals_df = edited

return_rate = st.slider("Expected annual return %", 6.0, 15.0, 12.0, 0.5)

plans = []
for _, row in edited.iterrows():
    if not row.get("Goal") or row.get("Target (₹)", 0) <= 0:
        continue
    p = plan_goal(
        name=str(row["Goal"]),
        target=float(row["Target (₹)"]),
        years=int(row["Years"]),
        priority=int(row["Priority"]),
        current_saved=float(row.get("Saved (₹)", 0)),
        allocated_sip=float(row.get("Your SIP (₹)", 0)),
        annual_return=return_rate,
    )
    plans.append(p)

if not plans:
    st.info("Add at least one goal to see your plan.")
    st.stop()

total_required = sum(p.required_monthly_sip for p in plans)
total_allocated = sum(float(r.get("Your SIP (₹)", 0)) for _, r in edited.iterrows())
gap = max(0, total_required - total_allocated)
st.session_state.goals_gap_total = gap

m1, m2, m3, m4 = st.columns(4)
m1.metric("Goals", len(plans))
m2.metric("SIP required", f"₹{total_required:,.0f}/mo")
m3.metric("Your allocation", f"₹{total_allocated:,.0f}/mo")
m4.metric("Gap", f"₹{gap:,.0f}/mo", delta=f"-{gap:,.0f}" if gap else "On track", delta_color="inverse" if gap else "normal")

if total_allocated > total_sip:
    st.warning(f"Goal SIPs (₹{total_allocated:,.0f}) exceed profile SIP (₹{total_sip:,.0f}). Adjust in sidebar profile.")

st.markdown("---")

# Goal cards + row lookup
row_by_goal = {str(r["Goal"]): r for _, r in edited.iterrows() if r.get("Goal")}

for p in sorted(plans, key=lambda x: x.priority):
    row = row_by_goal.get(p.name, {})
    user_sip = float(row.get("Your SIP (₹)", 0))
    saved = float(row.get("Saved (₹)", 0))
    col_a, col_b = st.columns([2, 1])
    with col_a:
        status = "✅ On track" if p.on_track else f"⚠️ Need ₹{p.gap_monthly:,.0f}/mo more"
        st.markdown(
            f"""<div class="glass-card">
            <strong>{p.name}</strong> <span style="float:right;color:{'#00d4aa' if p.on_track else '#fbbf24'};">{status}</span>
            <p style="color:#94a3b8;">Target ₹{p.target:,.0f} · {p.years}y · {p.recommended_asset}</p>
            <p>Required SIP: <strong>₹{p.required_monthly_sip:,.0f}/mo</strong></p></div>""",
            unsafe_allow_html=True,
        )
    with col_b:
        prob = probability_of_reaching_goal(
            user_sip or p.required_monthly_sip, saved, p.years, p.target,
            mean_return=return_rate / 100, simulations=400,
        )
        st.metric("Success odds", f"{prob*100:.0f}%")

fig = go.Figure()
colors = ["#00d4aa", "#8b5cf6", "#fbbf24", "#f43f5e", "#4facfe"]
for i, p in enumerate(plans):
    row = row_by_goal.get(p.name, {})
    saved = float(row.get("Saved (₹)", 0))
    sip_amt = float(row.get("Your SIP (₹)", 0)) or p.required_monthly_sip
    r = return_rate / 100 / 12
    years_x = list(range(p.years + 1))
    corpus = []
    bal = saved
    corpus.append(bal)
    for y in range(1, p.years + 1):
        for _ in range(12):
            bal = bal * (1 + r) + sip_amt
        corpus.append(bal)
    fig.add_trace(go.Scatter(x=years_x, y=corpus, mode="lines+markers", name=p.name, line=dict(color=colors[i % len(colors)], width=2)))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    height=420,
    title="Goal trajectory vs target",
    xaxis_title="Years",
    yaxis_title="₹",
    legend=dict(orientation="h", y=1.08),
)
st.plotly_chart(fig, use_container_width=True)

# Summary table
summary = pd.DataFrame(
    [
        {
            "Goal": p.name,
            "Target": f"₹{p.target:,.0f}",
            "Required SIP": f"₹{p.required_monthly_sip:,.0f}",
            "Your SIP": f"₹{float(row_by_goal.get(p.name, {}).get('Your SIP (₹)', 0)):,.0f}",
            "Asset mix": p.recommended_asset,
            "Status": "On track" if p.on_track else "Underfunded",
        }
        for p in plans
    ]
)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.download_button(
    "📥 Download goal plan (CSV)",
    summary.to_csv(index=False).encode(),
    "goal_plan.csv",
    "text/csv",
)
