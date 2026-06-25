export function ErrorAlert({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-200">
      <p className="font-medium">⚠️ {message}</p>
      {onRetry && (
        <button type="button" onClick={onRetry} className="mt-2 text-accent underline">
          Retry
        </button>
      )}
    </div>
  );
}
