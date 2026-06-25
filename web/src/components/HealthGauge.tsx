export function HealthGauge({
  score,
  grade,
  color,
}: {
  score: number;
  grade: string;
  color: string;
}) {
  const pct = score;
  return (
    <div className="flex flex-col items-center">
      <div
        className="relative flex h-36 w-36 items-center justify-center rounded-full border-4"
        style={{ borderColor: color }}
      >
        <div className="text-center">
          <div className="font-mono text-4xl font-bold" style={{ color }}>
            {score}
          </div>
          <div className="text-xs text-slate-400">/ 100</div>
        </div>
      </div>
      <p className="mt-3 font-semibold" style={{ color }}>
        {grade}
      </p>
      <div className="mt-2 h-2 w-full max-w-xs overflow-hidden rounded-full bg-white/10">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
      </div>
    </div>
  );
}
