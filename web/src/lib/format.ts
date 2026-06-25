export function formatINR(n: number): string {
  return `₹${n.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
}

export function formatINRDecimal(price: number): string {
  if (price >= 1000) return `₹${price.toLocaleString("en-IN", { minimumFractionDigits: 2 })}`;
  return `₹${price.toFixed(2)}`;
}

export function formatUSD(price: number): string {
  if (price >= 1000) return `$${price.toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
  if (price >= 1) return `$${price.toFixed(4)}`;
  return `$${price.toFixed(6)}`;
}

export function formatPct(n: number, digits = 2): string {
  const sign = n >= 0 ? "+" : "";
  return `${sign}${n.toFixed(digits)}%`;
}

export function currentWealth(profile: {
  profile_mf_value: number;
  profile_crypto_usd: number;
  profile_usd_inr: number;
}): number {
  return profile.profile_mf_value + profile.profile_crypto_usd * profile.profile_usd_inr;
}
