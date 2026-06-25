"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { MonteCarloResult } from "@/lib/types";
import { formatINR } from "@/lib/format";

export function MonteCarloChart({ data }: { data: MonteCarloResult }) {
  const chartData = data.months.map((m, i) => ({
    month: m,
    p10: data.p10[i],
    p50: data.p50[i],
    p90: data.p90[i],
  }));

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer>
        <AreaChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
          <XAxis
            dataKey="month"
            tickFormatter={(v) => `${Math.floor(v / 12)}y`}
            stroke="#94a3b8"
            fontSize={11}
          />
          <YAxis tickFormatter={(v) => `₹${(v / 100000).toFixed(0)}L`} stroke="#94a3b8" fontSize={11} />
          <Tooltip
            formatter={(v: number) => formatINR(v)}
            labelFormatter={(l) => `Month ${l}`}
            contentStyle={{ background: "#0a0e17", border: "1px solid rgba(255,255,255,0.1)" }}
          />
          <Legend />
          <Area type="monotone" dataKey="p90" stackId="1" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.15} name="P90" />
          <Area type="monotone" dataKey="p50" stackId="2" stroke="#00d4aa" fill="#00d4aa" fillOpacity={0.25} name="Median" />
          <Area type="monotone" dataKey="p10" stackId="3" stroke="#fbbf24" fill="#fbbf24" fillOpacity={0.1} name="P10" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
