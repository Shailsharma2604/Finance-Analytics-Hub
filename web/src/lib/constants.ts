import type { Profile } from "./types";

export const DEFAULT_PROFILE: Profile = {
  profile_age: 30,
  profile_income: 100_000,
  profile_sip: 25_000,
  profile_equity: 65,
  profile_mf_value: 500_000,
  profile_crypto_usd: 2_500,
  profile_emergency_fund: false,
  profile_insurance: false,
  profile_usd_inr: 83,
  profile_wealth_target: 5_000_000,
  profile_profit_target: 0,
  profile_target_years: 15,
  profile_target_mode: "wealth",
  profile_risk: "auto",
  profile_expected_return: 12,
  profile_mf_risk: "moderate",
  profile_equity_strategy: "balanced_growth",
  plan_applied: false,
  recommended_plan: null,
};

export const CRYPTO_OPTIONS: Record<string, string> = {
  "Bitcoin (BTC)": "BTCUSDT",
  "Ethereum (ETH)": "ETHUSDT",
  BNB: "BNBUSDT",
  "Solana (SOL)": "SOLUSDT",
  XRP: "XRPUSDT",
  "Cardano (ADA)": "ADAUSDT",
  "Dogecoin (DOGE)": "DOGEUSDT",
  "Polkadot (DOT)": "DOTUSDT",
  "Polygon (MATIC)": "MATICUSDT",
  "Avalanche (AVAX)": "AVAXUSDT",
};

export const WATCHLIST: [string, string][] = [
  ["BTC", "BTCUSDT"],
  ["ETH", "ETHUSDT"],
  ["BNB", "BNBUSDT"],
  ["SOL", "SOLUSDT"],
  ["XRP", "XRPUSDT"],
  ["ADA", "ADAUSDT"],
  ["DOGE", "DOGEUSDT"],
  ["DOT", "DOTUSDT"],
  ["MATIC", "MATICUSDT"],
  ["AVAX", "AVAXUSDT"],
];
