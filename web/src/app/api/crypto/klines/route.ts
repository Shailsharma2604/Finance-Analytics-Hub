import { NextRequest, NextResponse } from "next/server";
import { fetchCryptoKlines } from "@/lib/crypto-fetch";

export const revalidate = 300;

export async function GET(req: NextRequest) {
  const symbol = req.nextUrl.searchParams.get("symbol") ?? "BTCUSDT";
  const interval = req.nextUrl.searchParams.get("interval") ?? "1h";
  const limit = Number(req.nextUrl.searchParams.get("limit") ?? "168");

  try {
    const result = await fetchCryptoKlines(symbol, interval, limit);
    return NextResponse.json(result);
  } catch (e) {
    const message = e instanceof Error ? e.message : "Failed to fetch klines";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
