export function AppLayout({ sidebar, main, details }) {
  return (
    <main className="grid h-screen grid-cols-[280px_minmax(0,1fr)_320px] overflow-hidden bg-stone-100 text-stone-950">
      <aside className="border-r border-stone-200 bg-stone-950 text-stone-50">{sidebar}</aside>
      <section className="min-w-0 bg-[#f7f8f5]">{main}</section>
      <aside className="border-l border-stone-200 bg-white">{details}</aside>
    </main>
  );
}

