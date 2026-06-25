"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

const COLORS = ["#00d4aa", "#8b5cf6", "#fbbf24", "#34d399", "#fb923c", "#f43f5e"];

export function AllocationPie({
  data,
}: {
  data: { name: string; value: number }[];
}) {
  const filtered = data.filter((d) => d.value > 0);
  return (
    <div className="h-64 w-full">
      <ResponsiveContainer>
        <PieChart>
          <Pie data={filtered} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
            {filtered.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v: number) => `₹${v.toLocaleString("en-IN")}`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
