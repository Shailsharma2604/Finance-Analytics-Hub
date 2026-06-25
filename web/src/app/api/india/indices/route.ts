import { NextResponse } from "next/server";

const INDICES: Record<string, string> = {
  "Nifty 50": "%5ENSEI",
  Sensex: "%5EBSESN",
  "Bank Nifty": "%5ENSEBANK",
  "Nifty IT": "%5ENSEIT",
};

export const revalidate = 300;

async function fetchChart(symbolEncoded: string) {
  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbolEncoded}?interval=1d&range=5d`;
  const r = await fetch(url, {
    next: { revalidate: 300 },
    headers: { "User-Agent": "Mozilla/5.0 FinanceAnalyticsHub/1.0" },
  });
  if (!r.ok) return null;
  const json = await r.json();
  const result = json.chart?.result?.[0];
  if (!result) return null;
  const meta = result.meta;
  const closes = (result.indicators?.quote?.[0]?.close ?? []).filter(
    (c: number | null) => c != null
  ) as number[];
  const prev =
    closes.length >= 2 ? closes[closes.length - 2] : meta.chartPreviousClose ?? meta.regularMarketPrice;
  const price = meta.regularMarketPrice;
  const chg = prev ? ((price - prev) / prev) * 100 : 0;
  return {
    price,
    change_pct: chg,
    currency: meta.currency ?? "INR",
    sparkline: closes.slice(-5),
  };
}

export async function GET() {
  try {
    const results = await Promise.all(
      Object.entries(INDICES).map(async ([name, sym]) => {
        const data = await fetchChart(sym);
        return data ? { name, ...data } : null;
      })
    );
    const indices = results.filter(Boolean);
    if (indices.length === 0) {
      return NextResponse.json(
        { error: "Yahoo Finance unavailable — indices could not be loaded" },
        { status: 502 }
      );
    }
    return NextResponse.json({ indices });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch indices";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
