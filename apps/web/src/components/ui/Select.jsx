export function Select({ className = "", children, ...props }) {
  return (
    <select
      className={`h-9 rounded-md border border-stone-200 bg-white px-2 text-sm outline-none focus:border-emerald-700 focus:ring-2 focus:ring-emerald-100 ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}

