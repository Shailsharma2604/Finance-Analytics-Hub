import type { EquityStrategy, FundAllocation, AllocationPlan } from "./types";

type RiskProfile = "conservative" | "moderate" | "aggressive";

const EQUITY_TEMPLATES: Record<EquityStrategy, Record<string, number>> = {
  index_core: { index: 100 },
  market_weighted: { largecap: 70, midcap: 20, smallcap: 10 },
  balanced_growth: { largecap: 45, midcap: 30, smallcap: 25 },
  aggressive_growth: { largecap: 35, midcap: 35, smallcap: 30 },
};

const RECOMMENDED_FUNDS: Record<string, string[]> = {
  index: ["Nifty 50 Index Fund", "Sensex Index Fund"],
  largecap: ["Large Cap Fund", "Bluechip Fund"],
  midcap: ["Mid Cap Fund"],
  smallcap: ["Small Cap Fund"],
  FD: ["Bank FD / Debt Fund"],
};

function equityFromRisk(risk: RiskProfile): number {
  if (risk === "conservative") return 30;
  if (risk === "moderate") return 60;
  return 80;
}

function ageBasedStrategy(age: number): EquityStrategy {
  if (age < 35) return "aggressive_growth";
  if (age < 50) return "balanced_growth";
  return "market_weighted";
}

export function createAllocationPlan(params: {
  age: number;
  monthly_income: number;
  monthly_investment: number;
  risk_profile?: RiskProfile | null;
  custom_equity?: number | null;
  has_emergency_fund: boolean;
  has_insurance: boolean;
  equity_strategy?: EquityStrategy;
}): AllocationPlan {
  let equityPct: number;
  if (params.custom_equity != null) {
    equityPct = Math.max(0, Math.min(100, params.custom_equity));
  } else if (params.risk_profile) {
    equityPct = equityFromRisk(params.risk_profile);
  } else {
    equityPct = Math.max(20, Math.min(80, 100 - params.age));
  }
  const debtPct = 100 - equityPct;

  const strategy = params.equity_strategy ?? ageBasedStrategy(params.age);
  const template = EQUITY_TEMPLATES[strategy];

  const equityAllocations: Record<string, FundAllocation> = {};
  for (const [fundType, templatePct] of Object.entries(template)) {
    const actualPct = (templatePct / 100) * equityPct;
    equityAllocations[fundType] = {
      category: "Equity",
      subcategory: fundType.charAt(0).toUpperCase() + fundType.slice(1).replace("_", " "),
      percentage: Math.round(actualPct * 100) / 100,
      amount: Math.round((actualPct / 100) * params.monthly_investment),
      recommended_funds: RECOMMENDED_FUNDS[fundType] ?? [],
    };
  }

  const debtAllocations: Record<string, FundAllocation> = {
    FD: {
      category: "Debt",
      subcategory: "FD",
      percentage: debtPct,
      amount: Math.round((debtPct / 100) * params.monthly_investment),
      recommended_funds: RECOMMENDED_FUNDS.FD,
    },
  };

  const monthly_sip_breakdown: Record<string, number> = {};
  for (const [k, v] of Object.entries({ ...equityAllocations, ...debtAllocations })) {
    monthly_sip_breakdown[k] = v.amount;
  }

  const warnings: string[] = [];
  if (!params.has_emergency_fund && equityPct > 50) {
    warnings.push(
      "CRITICAL: Build 6 months of emergency fund before investing heavily in equity."
    );
  }
  if (!params.has_insurance) {
    warnings.push(
      "IMPORTANT: Ensure adequate term life and health insurance before aggressive equity allocation."
    );
  }
  if (equityPct > 80) {
    warnings.push("Very high equity allocation (>80%). Expect significant volatility.");
  }
  if (params.age > 60 && equityPct > 50) {
    warnings.push("At age 60+, consider reducing equity exposure for capital preservation.");
  }

  const recommendations = [
    "Keep portfolio simple with 5-7 funds total.",
    "Review portfolio annually; rebalance when allocation drifts 5-10% from target.",
    "Never try to time the market — maintain SIP discipline.",
    "Use low-cost index funds (Nifty 50/Sensex) as core equity holdings.",
    "Align investments with goals: short-term → debt, long-term → equity.",
  ];

  return {
    equity_percentage: Math.round(equityPct * 100) / 100,
    debt_percentage: Math.round(debtPct * 100) / 100,
    equity_allocations: equityAllocations,
    debt_allocations: debtAllocations,
    monthly_sip_breakdown,
    warnings,
    recommendations,
  };
}

export function projectRetirement(
  monthlySip: number,
  currentCorpus: number,
  years: number,
  annualReturn = 0.12
): { corpus: number; invested: number; gains: number } {
  const months = years * 12;
  const r = annualReturn / 12;
  let fv = currentCorpus * Math.pow(1 + r, months);
  if (r === 0) fv += monthlySip * months;
  else fv += monthlySip * ((Math.pow(1 + r, months) - 1) / r) * (1 + r);
  const invested = currentCorpus + monthlySip * months;
  return { corpus: fv, invested, gains: fv - invested };
}
