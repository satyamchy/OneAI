export function Button({ className = "", variant = "primary", ...props }) {
  const variants = {
    primary: "bg-emerald-700 text-white hover:bg-emerald-800",
    secondary: "bg-white text-stone-800 border border-stone-200 hover:bg-stone-50",
    ghost: "text-stone-700 hover:bg-stone-100",
    danger: "bg-red-600 text-white hover:bg-red-700"
  };

  return (
    <button
      className={`inline-flex h-9 items-center justify-center gap-2 rounded-md px-3 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    />
  );
}

