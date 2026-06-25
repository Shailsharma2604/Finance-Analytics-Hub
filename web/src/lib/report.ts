import type { Profile } from "./types";

export function buildHtmlReport(params: {
  profile: Profile;
  health_score: number;
  health_grade: string;
  insights: string[];
  total_portfolio: number;
  mood_label: string;
  mood_score: number;
}): string {
  const { profile, health_score, health_grade, insights, total_portfolio, mood_label, mood_score } =
    params;
  const insightRows = insights.map((i) => `<li>${i}</li>`).join("");
  const now = new Date().toLocaleString("en-IN", {
    dateStyle: "long",
    timeStyle: "short",
  });

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Finance Analytics Hub — Report</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #0a0e17; color: #f1f5f9; padding: 2rem; max-width: 800px; margin: auto; }
    h1 { background: linear-gradient(135deg, #00d4aa, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; }
    .score { font-size: 3rem; font-weight: 800; color: #00d4aa; }
    table { width: 100%; border-collapse: collapse; }
    td { padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .muted { color: #94a3b8; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>Finance Analytics Hub</h1>
  <p class="muted">Generated ${now}</p>
  <div class="card">
    <p class="muted">Financial Health</p>
    <div class="score">${health_score}</div>
    <p><strong>${health_grade}</strong></p>
  </div>
  <div class="card">
    <h3>Profile Snapshot</h3>
    <table>
      <tr><td>Age</td><td>${profile.profile_age}</td></tr>
      <tr><td>Monthly income</td><td>₹${profile.profile_income.toLocaleString("en-IN")}</td></tr>
      <tr><td>Monthly SIP</td><td>₹${profile.profile_sip.toLocaleString("en-IN")}</td></tr>
      <tr><td>Equity target</td><td>${profile.profile_equity}%</td></tr>
      <tr><td>Portfolio value</td><td>₹${total_portfolio.toLocaleString("en-IN")}</td></tr>
      <tr><td>Crypto mood</td><td>${mood_label} (${mood_score}/100)</td></tr>
      <tr><td>Wealth target</td><td>₹${profile.profile_wealth_target.toLocaleString("en-IN")}</td></tr>
      <tr><td>Profit target (annual)</td><td>₹${profile.profile_profit_target.toLocaleString("en-IN")}</td></tr>
      <tr><td>Horizon</td><td>${profile.profile_target_years} years</td></tr>
      <tr><td>Risk profile</td><td>${profile.profile_mf_risk}</td></tr>
    </table>
  </div>
  <div class="card">
    <h3>Recommendations</h3>
    <ul>${insightRows}</ul>
  </div>
  <p class="muted">Educational use only — not financial advice.</p>
</body>
</html>`;
}

export function downloadHtmlReport(html: string, filename = "finance-report.html") {
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
