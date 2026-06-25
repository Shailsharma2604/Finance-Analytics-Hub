/** Seeded PRNG (mulberry32) for reproducible Monte Carlo */
function mulberry32(seed: number) {
  let s = seed;
  return () => {
    s += 0x6d2b79f5;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function randomNormal(rng: () => number, mean: number, stdDev: number): number {
  const u1 = rng();
  const u2 = rng();
  const z = Math.sqrt(-2 * Math.log(Math.max(u1, 1e-10))) * Math.cos(2 * Math.PI * u2);
  return mean + z * stdDev;
}

export function runMonteCarlo(
  monthlySip: number,
  lumpSum: number,
  years: number,
  meanReturn = 0.12,
  volatility = 0.18,
  simulations = 500,
  seed: number | null = 42
): import("./types").MonteCarloResult {
  const rng = seed !== null ? mulberry32(seed) : Math.random;
  const months = years * 12;
  const mu = meanReturn / 12;
  const sigma = volatility / Math.sqrt(12);

  const paths: number[][] = Array.from({ length: simulations }, () => new Array(months + 1).fill(0));
  for (let sim = 0; sim < simulations; sim++) {
    let balance = lumpSum;
    paths[sim][0] = balance;
    for (let m = 1; m <= months; m++) {
      const r = randomNormal(rng as () => number, mu, sigma);
      balance = balance * (1 + r) + monthlySip;
      paths[sim][m] = balance;
    }
  }

  const monthsAxis = Array.from({ length: months + 1 }, (_, i) => i);
  const percentile = (arr: number[], p: number) => {
    const sorted = [...arr].sort((a, b) => a - b);
    const idx = (p / 100) * (sorted.length - 1);
    const lo = Math.floor(idx);
    const hi = Math.ceil(idx);
    if (lo === hi) return sorted[lo];
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo);
  };

  const p10: number[] = [];
  const p50: number[] = [];
  const p90: number[] = [];
  for (let m = 0; m <= months; m++) {
    const col = paths.map((row) => row[m]);
    p10.push(percentile(col, 10));
    p50.push(percentile(col, 50));
    p90.push(percentile(col, 90));
  }

  const finals = paths.map((row) => row[months]);
  const invested = lumpSum + monthlySip * months;

  return {
    months: monthsAxis,
    p10,
    p50,
    p90,
    final_median: percentile(finals, 50),
    final_p10: percentile(finals, 10),
    final_p90: percentile(finals, 90),
    total_invested: invested,
  };
}

export function probabilityOfReachingGoal(
  monthlySip: number,
  lumpSum: number,
  years: number,
  goalAmount: number,
  meanReturn = 0.12,
  volatility = 0.18,
  simulations = 800
): number {
  const months = years * 12;
  const mu = meanReturn / 12;
  const sigma = volatility / Math.sqrt(12);
  let success = 0;
  for (let s = 0; s < simulations; s++) {
    let b = lumpSum;
    for (let m = 0; m < months; m++) {
      const u1 = Math.random();
      const u2 = Math.random();
      const z = Math.sqrt(-2 * Math.log(Math.max(u1, 1e-10))) * Math.cos(2 * Math.PI * u2);
      b = b * (1 + (mu + z * sigma)) + monthlySip;
    }
    if (b >= goalAmount) success++;
  }
  return success / simulations;
}
