export function Spinner({ className = "" }) {
  return (
    <span
      className={`inline-block h-4 w-4 animate-spin rounded-full border-2 border-stone-300 border-t-emerald-700 ${className}`}
    />
  );
}

