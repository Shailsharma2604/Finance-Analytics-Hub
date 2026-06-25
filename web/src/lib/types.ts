export type RiskChoice = "auto" | "conservative" | "moderate" | "aggressive";
export type TargetMode = "wealth" | "profit";
export type EquityStrategy =
  | "index_core"
  | "market_weighted"
  | "balanced_growth"
  | "aggressive_growth";

export interface Profile {
  profile_age: number;
  profile_income: number;
  profile_sip: number;
  profile_equity: number;
  profile_mf_value: number;
  profile_crypto_usd: number;
  profile_emergency_fund: boolean;
  profile_insurance: boolean;
  profile_usd_inr: number;
  profile_wealth_target: number;
  profile_profit_target: number;
  profile_target_years: number;
  profile_target_mode: TargetMode;
  profile_risk: RiskChoice;
  profile_expected_return: number;
  profile_mf_risk: string;
  profile_equity_strategy: EquityStrategy;
  plan_applied?: boolean;
  recommended_plan?: RecommendedPlan | null;
}

export interface RecommendedPlan {
  target_mode: string;
  wealth_target: number;
  profit_target_annual: number;
  target_years: number;
  current_wealth: number;
  required_monthly_sip: number;
  recommended_sip: number;
  equity_pct: number;
  mf_pct: number;
  crypto_pct: number;
  liquid_pct: number;
  risk_profile: string;
  equity_strategy: string;
  mf_sip: number;
  crypto_sip: number;
  liquid_sip: number;
  expected_annual_profit: number;
  median_corpus_at_horizon: number;
  success_probability: number;
  on_track: boolean;
  gap_monthly: number;
  savings_rate_pct: number;
  plan_grade: string;
  summary: string;
  actions: string[];
}

export interface GoalRow {
  id: string;
  goal: string;
  target: number;
  years: number;
  priority: number;
  saved: number;
  sip: number;
}

export interface GoalPlan {
  name: string;
  target: number;
  years: number;
  priority: number;
  required_monthly_sip: number;
  recommended_asset: string;
  on_track: boolean;
  gap_monthly: number;
}

export interface HealthResult {
  score: number;
  grade: string;
  color: string;
  breakdown: Record<string, number>;
  insights: string[];
}

export interface AdvisorInsight {
  priority: number;
  category: string;
  title: string;
  body: string;
  action: string;
}

export interface MarketMood {
  score: number;
  label: string;
  color: string;
  details: Record<string, string>;
}

export interface MonteCarloResult {
  months: number[];
  p10: number[];
  p50: number[];
  p90: number[];
  final_median: number;
  final_p10: number;
  final_p90: number;
  total_invested: number;
}

export interface FundAllocation {
  category: string;
  subcategory: string;
  percentage: number;
  amount: number;
  recommended_funds: string[];
}

export interface AllocationPlan {
  equity_percentage: number;
  debt_percentage: number;
  equity_allocations: Record<string, FundAllocation>;
  debt_allocations: Record<string, FundAllocation>;
  monthly_sip_breakdown: Record<string, number>;
  warnings: string[];
  recommendations: string[];
}

export interface CryptoTicker {
  symbol: string;
  lastPrice: string;
  priceChangePercent: string;
  quoteVolume: string;
}

export interface IndiaIndex {
  name: string;
  price: number;
  change_pct: number;
  currency: string;
  sparkline: number[];
}

export interface PaperHolding {
  symbol: string;
  label: string;
  qty: number;
  avgPrice: number;
}
