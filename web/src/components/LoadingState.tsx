export function LoadingState({ label = "Loading market data…" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-6">
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-accent border-t-transparent" />
      <span className="text-sm text-slate-400">{label}</span>
    </div>
  );
}
