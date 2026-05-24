# 🎓 Finance Analytics Hub

### Final Year Project · B.Tech Computer Science · 2025–26

**An Intelligent Web-Based Platform for Personal Investment Planning & Portfolio Analytics**

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

1. Build a unified fintech dashboard with 7 functional modules  
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

## Installation

```bash
git clone <your-repo>
cd main_project
pip install -r requirements.txt
streamlit run main.py
```

Open **http://localhost:8501**

### Demo mode (for viva)

1. Open the app → click **Start demo walkthrough** on home  
2. Or sidebar → **Load demo profile**  
3. Walk through: **Command Center** → **Goal Planner** → **AI Advisor**

## Project Structure

```
main_project/
├── main.py                 # Landing page
├── pages/                  # 7 Streamlit pages
├── lib/                    # Shared engines & theme
├── MutualFunds-.../        # Allocation engine
├── requirements.txt
└── README.md
```

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
