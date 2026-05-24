"""HTML financial report export."""

from __future__ import annotations

from datetime import datetime


def build_html_report(
    profile: dict,
    health_score: int,
    health_grade: str,
    insights: list[str],
    total_portfolio: float,
    mood_label: str,
    mood_score: int,
) -> str:
    insight_rows = "".join(f"<li>{i}</li>" for i in insights)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Finance Analytics Hub — Report</title>
  <style>
    body {{ font-family: 'Segoe UI', sans-serif; background: #0a0e17; color: #f1f5f9; padding: 2rem; max-width: 800px; margin: auto; }}
    h1 {{ background: linear-gradient(135deg, #00d4aa, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .card {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }}
    .score {{ font-size: 3rem; font-weight: 800; color: #00d4aa; }}
    table {{ width: 100%; border-collapse: collapse; }}
    td {{ padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); }}
    .muted {{ color: #94a3b8; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>💎 Finance Analytics Hub</h1>
  <p class="muted">Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>

  <div class="card">
    <p class="muted">Financial Health</p>
    <div class="score">{health_score}</div>
    <p><strong>{health_grade}</strong></p>
  </div>

  <div class="card">
    <h3>Profile Snapshot</h3>
    <table>
      <tr><td>Age</td><td>{profile.get('profile_age')}</td></tr>
      <tr><td>Monthly income</td><td>₹{profile.get('profile_income', 0):,.0f}</td></tr>
      <tr><td>Monthly SIP</td><td>₹{profile.get('profile_sip', 0):,.0f}</td></tr>
      <tr><td>Equity target</td><td>{profile.get('profile_equity')}%</td></tr>
      <tr><td>Portfolio value</td><td>₹{total_portfolio:,.0f}</td></tr>
      <tr><td>Crypto mood</td><td>{mood_label} ({mood_score}/100)</td></tr>
    </table>
  </div>

  <div class="card">
    <h3>Recommendations</h3>
    <ul>{insight_rows}</ul>
  </div>

  <p class="muted">Educational use only — not financial advice.</p>
</body>
</html>"""
