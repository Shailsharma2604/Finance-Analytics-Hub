"use client";

import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface Candle {
  time: string;
  close: number;
}

export function CryptoPriceChart({ candles, symbol }: { candles: Candle[]; symbol: string }) {
  const data = candles.map((c) => ({
    time: new Date(c.time).toLocaleDateString("en-IN", { month: "short", day: "numeric", hour: "2-digit" }),
    close: c.close,
  }));

  return (
    <div className="h-72 w-full">
      <p className="mb-2 text-sm text-slate-400">{symbol} — hourly close</p>
      <ResponsiveContainer>
        <LineChart data={data}>
          <XAxis dataKey="time" hide />
          <YAxis domain={["auto", "auto"]} stroke="#94a3b8" fontSize={11} tickFormatter={(v) => `$${v.toLocaleString()}`} />
          <Tooltip
            formatter={(v: number) => [`$${v.toLocaleString()}`, "Close"]}
            contentStyle={{ background: "#0a0e17", border: "1px solid rgba(255,255,255,0.1)" }}
          />
          <Line type="monotone" dataKey="close" stroke="#00d4aa" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
