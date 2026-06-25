import { NextResponse } from "next/server";

const BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/24hr";

export const revalidate = 60;

export async function GET() {
  try {
    const resp = await fetch(BINANCE_TICKER, {
      next: { revalidate: 60 },
      headers: { Accept: "application/json" },
    });
    if (!resp.ok) {
      return NextResponse.json(
        { error: "Binance API unavailable", status: resp.status },
        { status: 502 }
      );
    }
    const data = await resp.json();
    return NextResponse.json(data);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch crypto data";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
