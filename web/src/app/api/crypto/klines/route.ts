import { NextRequest, NextResponse } from "next/server";

const BINANCE_KLINES = "https://api.binance.com/api/v3/klines";

export const revalidate = 300;

export async function GET(req: NextRequest) {
  const symbol = req.nextUrl.searchParams.get("symbol") ?? "BTCUSDT";
  const interval = req.nextUrl.searchParams.get("interval") ?? "1h";
  const limit = req.nextUrl.searchParams.get("limit") ?? "168";

  try {
    const url = new URL(BINANCE_KLINES);
    url.searchParams.set("symbol", symbol);
    url.searchParams.set("interval", interval);
    url.searchParams.set("limit", limit);

    const resp = await fetch(url.toString(), {
      next: { revalidate: 300 },
      headers: { Accept: "application/json" },
    });
    if (!resp.ok) {
      return NextResponse.json(
        { error: "Binance klines unavailable", status: resp.status },
        { status: 502 }
      );
    }
    const raw = await resp.json();
    const candles = raw.map((c: (string | number)[]) => ({
      time: new Date(Number(c[0])).toISOString(),
      open: parseFloat(String(c[1])),
      high: parseFloat(String(c[2])),
      low: parseFloat(String(c[3])),
      close: parseFloat(String(c[4])),
      volume: parseFloat(String(c[5])),
    }));
    return NextResponse.json({ symbol, interval, candles });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch klines";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
