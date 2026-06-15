export function Textarea({ className = "", ...props }) {
  return (
    <textarea
      className={`w-full resize-none rounded-md border border-stone-200 bg-white px-3 py-2 text-sm outline-none transition placeholder:text-stone-400 focus:border-emerald-700 focus:ring-2 focus:ring-emerald-100 ${className}`}
      {...props}
    />
  );
}

