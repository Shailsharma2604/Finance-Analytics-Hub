"""Monte Carlo wealth simulation."""

from __future__ import annotations

import numpy as np
import pandas as pd


def run_monte_carlo(
    monthly_sip: float,
    lump_sum: float,
    years: int,
    mean_return: float = 0.12,
    volatility: float = 0.18,
    simulations: int = 500,
    seed: int | None = 42,
) -> dict:
    """
    Simulate monthly SIP + lump sum with lognormal monthly returns.
    Returns percentile paths and summary stats.
    """
    if seed is not None:
        np.random.seed(seed)

    months = years * 12
    mu = mean_return / 12
    sigma = volatility / np.sqrt(12)

    paths = np.zeros((simulations, months + 1))
    paths[:, 0] = lump_sum

    for sim in range(simulations):
        balance = lump_sum
        for m in range(1, months + 1):
            r = np.random.normal(mu, sigma)
            balance = balance * (1 + r) + monthly_sip
            paths[sim, m] = balance

    months_axis = np.arange(months + 1)
    p10 = np.percentile(paths, 10, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p90 = np.percentile(paths, 90, axis=0)

    final = paths[:, -1]
    invested = lump_sum + monthly_sip * months

    return {
        "months": months_axis,
        "p10": p10,
        "p50": p50,
        "p90": p90,
        "paths_sample": paths[: min(30, simulations)],
        "final_median": float(np.median(final)),
        "final_p10": float(np.percentile(final, 10)),
        "final_p90": float(np.percentile(final, 90)),
        "total_invested": invested,
        "probability_goal": None,  # set externally if goal provided
    }


def probability_of_reaching_goal(
    monthly_sip: float,
    lump_sum: float,
    years: int,
    goal_amount: float,
    **kwargs,
) -> float:
    """Fraction of simulations that meet or exceed goal at horizon."""
    if seed := kwargs.get("seed"):
        np.random.seed(seed)
    sims = kwargs.get("simulations", 800)
    result = run_monte_carlo(monthly_sip, lump_sum, years, simulations=sims, seed=None)
    # Re-run with more sims for probability only
    months = years * 12
    mu = kwargs.get("mean_return", 0.12) / 12
    sigma = kwargs.get("volatility", 0.18) / np.sqrt(12)
    finals = []
    for _ in range(sims):
        b = lump_sum
        for _ in range(months):
            b = b * (1 + np.random.normal(mu, sigma)) + monthly_sip
        finals.append(b)
    return float(np.mean(np.array(finals) >= goal_amount))
