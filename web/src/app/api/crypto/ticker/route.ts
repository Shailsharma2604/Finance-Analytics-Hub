import { NextResponse } from "next/server";
import { fetchCryptoTickers } from "@/lib/crypto-fetch";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const { tickers, source } = await fetchCryptoTickers();
    return NextResponse.json({ tickers, source });
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch crypto data";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
