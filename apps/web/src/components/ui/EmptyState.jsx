export function EmptyState({ title, description }) {
  return (
    <div className="flex h-full flex-col items-center justify-center px-8 text-center">
      <h2 className="text-lg font-semibold text-stone-900">{title}</h2>
      {description ? <p className="mt-2 max-w-sm text-sm text-stone-500">{description}</p> : null}
    </div>
  );
}

