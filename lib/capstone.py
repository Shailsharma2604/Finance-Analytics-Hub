"""Capstone presentation components — headers, footers, stats."""

from __future__ import annotations

import streamlit as st
from lib.project_meta import PROJECT, TECH_STACK


def render_capstone_footer():
    st.markdown(
        f"""
        <div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid rgba(255,255,255,0.08);margin-top:2rem;">
            <p style="color:#64748b;font-size:0.85rem;margin:0;">
                <strong style="color:#94a3b8;">{PROJECT['title']}</strong> · {PROJECT['batch']} · {PROJECT['academic_year']}<br>
                Submitted by <strong style="color:#00d4aa;">{PROJECT['student_name']}</strong>
                ({PROJECT['roll_number']}) · {PROJECT['department']}<br>
                Under the guidance of {PROJECT['guide_name']} · {PROJECT['institution']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_demo_banner():
    if st.session_state.get("demo_loaded"):
        st.success("🎬 **Demo mode** — sample profile loaded. Perfect for presentation walkthrough.")


def render_tech_badges():
    badges = " ".join(
        f'<span class="tech-badge">{name}</span>' for name, _ in TECH_STACK
    )
    st.markdown(f'<div style="text-align:center;margin:1rem 0;">{badges}</div>', unsafe_allow_html=True)
