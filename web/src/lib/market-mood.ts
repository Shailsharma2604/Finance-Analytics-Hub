import type { CryptoTicker, MarketMood } from "./types";

export function computeMarketMood(tickers: CryptoTicker[]): MarketMood {
  const usdt = tickers.filter((t) => t.symbol.endsWith("USDT"));
  if (usdt.length === 0) {
    return { score: 50, label: "Neutral", color: "#fbbf24", details: {} };
  }

  const liquid = usdt.filter((t) => parseFloat(t.quoteVolume) > 500_000);
  const pctPositive =
    (liquid.filter((t) => parseFloat(t.priceChangePercent) > 0).length / liquid.length) * 100;
  let avgChange =
    liquid.reduce((s, t) => s + parseFloat(t.priceChangePercent), 0) / liquid.length;
  avgChange = Math.max(-15, Math.min(15, avgChange));
  const avgNorm = ((avgChange + 15) / 30) * 100;

  const btcRow = usdt.find((t) => t.symbol === "BTCUSDT");
  const btcChange = btcRow ? parseFloat(btcRow.priceChangePercent) : 0;
  const btcNorm = ((Math.max(-10, Math.min(10, btcChange)) + 10) / 20) * 100;

  const volumes = liquid.map((t) => parseFloat(t.quoteVolume)).sort((a, b) => a - b);
  const volMedian = volumes[Math.floor(volumes.length / 2)] ?? 0;
  const highVol = liquid.filter((t) => parseFloat(t.quoteVolume) > volMedian * 2).length;
  const volStress = Math.max(0, 100 - (highVol / Math.max(liquid.length, 1)) * 200);

  let score = 0.35 * pctPositive + 0.3 * avgNorm + 0.25 * btcNorm + 0.1 * volStress;
  score = Math.round(Math.max(0, Math.min(100, score)));

  let label: string;
  let color: string;
  if (score >= 75) [label, color] = ["Extreme Greed", "#00d4aa"];
  else if (score >= 55) [label, color] = ["Greed", "#34d399"];
  else if (score >= 45) [label, color] = ["Neutral", "#fbbf24"];
  else if (score >= 25) [label, color] = ["Fear", "#fb923c"];
  else [label, color] = ["Extreme Fear", "#f43f5e"];

  return {
    score,
    label,
    color,
    details: {
      pairs_rising: `${pctPositive.toFixed(0)}%`,
      avg_change: `${avgChange >= 0 ? "+" : ""}${avgChange.toFixed(2)}%`,
      btc_24h: `${btcChange >= 0 ? "+" : ""}${btcChange.toFixed(2)}%`,
    },
  };
}

export function topMovers(
  tickers: CryptoTicker[],
  quote = "USDT",
  n = 5
): { gainers: CryptoTicker[]; losers: CryptoTicker[] } {
  const usdt = tickers
    .filter((t) => t.symbol.endsWith(quote))
    .filter((t) => parseFloat(t.quoteVolume) > 1_000_000)
    .map((t) => ({
      ...t,
      priceChangePercent: String(parseFloat(t.priceChangePercent)),
      lastPrice: String(parseFloat(t.lastPrice)),
      quoteVolume: String(parseFloat(t.quoteVolume)),
    }));

  const sorted = [...usdt].sort(
    (a, b) => parseFloat(b.priceChangePercent) - parseFloat(a.priceChangePercent)
  );
  return {
    gainers: sorted.slice(0, n),
    losers: sorted.slice(-n).reverse(),
  };
}
