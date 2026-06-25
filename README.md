# 🎓 Finance Analytics Hub

### Final Year Project · B.Tech Computer Science · 2025–26

**An Intelligent Web-Based Platform for Personal Investment Planning & Portfolio Analytics**

> **Full project documentation:** see **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** — architecture, all 8 modules, algorithms, session state, APIs, demo mode, and viva tips.

---

| | |
|---|---|
| **Student** | Shail · CS-FYP-2026-001 |
| **Department** | Computer Science & Engineering |
| **Guide** | Dr. [Guide Name] |
| **Institution** | [Your University Name] |

---

## Abstract

This project presents **Finance Analytics Hub**, a unified web application that helps retail investors plan mutual fund allocations, track cryptocurrency markets, set multi-goal SIP targets, and assess financial health — all through a single Streamlit interface. The system integrates live data from **Binance** (crypto) and **Yahoo Finance** (Nifty 50, Sensex), implements a **Monte Carlo wealth simulator**, and provides an **explainable AI-style advisor** based on user profile and market mood. The platform is designed as an educational decision-support tool, not a substitute for licensed financial advice.

## Problem Statement

Investors use fragmented tools for mutual funds, crypto, and goal planning. There is a need for an integrated, visual, and quantitative platform that combines allocation logic, live markets, and personalized insights.

## Objectives

1. Build a unified fintech dashboard with 8 integrated modules (including Profile & Best Plan)  
2. Implement asset allocation engine with equity-debt split and SIP breakdown  
3. Integrate live market APIs without API keys  
4. Develop Monte Carlo and goal-based SIP calculators  
5. Create financial health scoring and exportable HTML reports  

## System Architecture

```
Streamlit UI  →  lib/ (shared logic)  →  Allocation Engine | Binance | Yahoo Finance
```

## Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | Project Overview | FYP documentation, architecture, demo mode |
| 2 | Command Center | India indices, crypto mood, Monte Carlo |
| 3 | Mutual Funds | Allocation planner, retirement projection |
| 4 | Crypto Intelligence | Charts, movers, paper portfolio |
| 5 | Goal Planner | Multi-goal SIP + success probability |
| 6 | AI Advisor | Prioritized insights + HTML report |
| 7 | Portfolio Pulse | Unified asset mix + health |

## Tech Stack

Python · Streamlit · Plotly · Pandas · NumPy · Requests · Binance API · Yahoo Finance  
**Production (Vercel):** Next.js 15 · TypeScript · Tailwind CSS · Recharts

## Deploy to Vercel

The **Streamlit app cannot run on Vercel** (long-running Python + WebSockets). Use the **`web/`** Next.js app for cloud deployment; keep Streamlit for local development.

### Prerequisites

- [Vercel account](https://vercel.com/signup)
- [Vercel CLI](https://vercel.com/docs/cli) (optional): `npm i -g vercel`

### Option A — Vercel Dashboard (recommended)

1. Push this repo to GitHub.
2. [Import project](https://vercel.com/new) → select the repository.
3. Set **Root Directory** to `web`.
4. Framework preset: **Next.js** (auto-detected).
5. Build command: `npm run build` · Install: `npm install` · Output: default (`.next`).
6. **Environment variables:** none required (Binance & Yahoo are keyless). Copy `.env.example` if you add optional tuning vars.
7. Deploy.

### Option B — Vercel CLI

```bash
cd web
npm install
npm run build          # verify locally first
vercel                 # link project on first run
vercel --prod          # production deploy
```

When prompted for the project root, use **`web`** (not the repo root).

### What runs where

| Runtime | Command | Use case |
|---------|---------|----------|
| **Vercel** (`web/`) | `npm run dev` / Vercel deploy | Public demo, FYP submission URL |
| **Local Streamlit** | `streamlit run main.py` | Full Python stack, allocation engine source |

### Monorepo note

`vercel.json` at the repo root points build commands at `web/`. If you set Root Directory to `web` in the dashboard, the root `vercel.json` is ignored — `web/vercel.json` applies instead.

## Installation (Streamlit — local)

```bash
git clone <your-repo>
cd Finance_Analytics_Hub
pip install -r requirements.txt
streamlit run main.py
```

Open **http://localhost:8501**

## Deploy

No API keys are required (Binance and Yahoo Finance are used without authentication). Outbound HTTPS must be allowed for live market data.

### Docker (recommended)

```bash
docker compose up --build
```

Or without Compose:

```bash
docker build -t finance-analytics-hub .
docker run -p 8501:8501 finance-analytics-hub
```

Open **http://localhost:8501**. Cloud hosts that set a `PORT` env var (Railway, Render, etc.) are supported automatically.

### Streamlit Community Cloud

**Repo:** [github.com/Shailsharma2604/Finance-Analytics-Hub](https://github.com/Shailsharma2604/Finance-Analytics-Hub)

No API keys or `.streamlit/secrets.toml` are required — Binance and Yahoo Finance are used without authentication.

#### 1. Push to GitHub

```bash
cd Finance_Analytics_Hub
git add main.py pages/ lib/ requirements.txt .streamlit/ MutualFunds-Allocation-Planner-main/
git commit -m "Prepare Streamlit Cloud deployment"
git push origin main
```

Skip `git commit` if everything is already pushed.

#### 2. Deploy on Streamlit Cloud

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
2. Click **Create app** (or **New app**).
3. Set:
   - **Repository:** `Shailsharma2604/Finance-Analytics-Hub`
   - **Branch:** `main`
   - **Main file path:** `main.py`
4. **Advanced settings** (optional): set **Python version** to **3.11** (matches the Docker image; 3.12 also works).
5. Leave **Secrets** empty — not needed for current features.
6. Click **Deploy**. First build takes a few minutes.

Your app will be live at `https://<app-name>.streamlit.app`.

#### Notes

- `packages.txt` is not required (no system-level apt dependencies).
- Live market data needs outbound HTTPS from Streamlit Cloud to Binance and Yahoo Finance.
- The embedded Mutual Funds planner ships inside `MutualFunds-Allocation-Planner-main/` — no git submodules.

### Demo mode (for viva)

1. Open the app → click **Start demo walkthrough** on home  
2. Or sidebar → **Load demo profile**  
3. Walk through: **Command Center** → **Goal Planner** → **AI Advisor**

## Project Structure

```
Finance_Analytics_Hub/
├── main.py                 # Streamlit landing (local)
├── pages/                  # 8 Streamlit pages
├── lib/                    # Shared Python engines & theme
├── web/                    # Next.js app (Vercel deployment)
│   ├── src/app/            # App Router pages + API routes
│   ├── src/lib/            # TypeScript ports of calculators
│   └── package.json
├── MutualFunds-.../        # Allocation engine (Python)
├── vercel.json             # Monorepo deploy hints
├── .env.example
├── requirements.txt
└── README.md
```

### Next.js (Vercel) — local dev

```bash
cd web
npm install
npm run dev
```

Open **http://localhost:3000**

## Screenshots

_Add screenshots before submission: Home, Command Center, Goal Planner, AI Advisor._

## Future Scope

- ML-based risk profiling  
- NSE equity screener  
- User authentication & cloud save  
- Mobile application  

## Disclaimer

Educational project only. Not SEBI-registered investment advice. Consult a certified financial advisor before investing.

---

**Submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology**
