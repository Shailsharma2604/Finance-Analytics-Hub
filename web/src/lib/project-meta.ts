export const PROJECT = {
  title: "Finance Analytics Hub",
  subtitle:
    "An Intelligent Web-Based Platform for Personal Investment Planning & Portfolio Analytics",
  student_name: "Shail",
  roll_number: "CS-FYP-2026-001",
  department: "Computer Science & Engineering",
  institution: "[Your University Name]",
  academic_year: "2025–26",
  guide_name: "Dr. [Guide Name]",
  batch: "B.Tech Final Year",
};

export const MODULES = [
  { name: "Profile & Plan", desc: "Wealth/profit targets → best SIP & allocation synced app-wide", href: "/profile", icon: "⚙️" },
  { name: "Command Center", desc: "Live indices, crypto mood, Monte Carlo engine", href: "/command-center", icon: "🏠" },
  { name: "Mutual Fund Planner", desc: "Equity-debt allocation, SIP, rebalancing", href: "/mutual-funds", icon: "📈" },
  { name: "Crypto Intelligence", desc: "OHLCV charts, movers, paper portfolio", href: "/crypto", icon: "₿" },
  { name: "Goal Planner", desc: "Multi-goal SIP with success probability", href: "/goals", icon: "🎯" },
  { name: "AI Advisor", desc: "Prioritized insights from profile + markets", href: "/advisor", icon: "🧠" },
  { name: "Portfolio Pulse", desc: "Unified dashboard & HTML reports", href: "/portfolio", icon: "💓" },
];

export const OBJECTIVES = [
  "Design a unified platform integrating mutual fund allocation and cryptocurrency analytics.",
  "Implement rule-based and Monte Carlo models for wealth projection and goal planning.",
  "Develop a financial health scoring system across five readiness pillars.",
  "Integrate live market data (Binance API, Indian indices) without proprietary keys.",
  "Provide exportable reports suitable for personal financial review.",
];

export const TECH_STACK = [
  ["Python 3.11 / TypeScript", "Core logic"],
  ["Streamlit + Next.js", "Web frameworks"],
  ["Plotly / Recharts", "Interactive charts"],
  ["Pandas / NumPy", "Data & simulation (Python)"],
  ["Binance API", "Crypto live data"],
  ["Yahoo Finance", "Nifty / Sensex"],
];
