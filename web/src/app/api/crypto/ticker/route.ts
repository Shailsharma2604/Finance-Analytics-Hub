import { NextResponse } from "next/server";

const BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const resp = await fetch(BINANCE_TICKER, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!resp.ok) {
      return NextResponse.json(
        { error: "Binance API unavailable", status: resp.status },
        { status: 502 }
      );
    }
    const data = await resp.json();
    // Return liquid USDT pairs only — full Binance payload exceeds Vercel 2MB cache limit
    const usdt = (data as { symbol: string; lastPrice: string; priceChangePercent: string; quoteVolume: string }[])
      .filter((t) => t.symbol.endsWith("USDT"));
    return NextResponse.json(usdt);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch crypto data";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
