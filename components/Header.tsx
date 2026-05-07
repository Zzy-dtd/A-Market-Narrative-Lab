export function Header({ onOpenSettings }: { onOpenSettings: () => void }) {
  return (
    <header className="mx-auto flex w-full max-w-6xl items-start justify-between gap-4 px-4 pt-6 sm:px-6">
      <div>
        <h1 className="text-3xl font-bold tracking-normal text-lab-text sm:text-4xl">
          Market Narrative Lab
        </h1>
        <p className="mt-2 text-base text-slate-600">
          Learn how different investors think, not copy their trades.
        </p>
        <p className="mt-2 text-sm text-slate-500">
          Educational analysis only. No buy/sell recommendations or price targets.
        </p>
      </div>
      <button
        type="button"
        onClick={onOpenSettings}
        className="rounded-full border border-slate-900/10 bg-white/80 px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-white"
      >
        Settings
      </button>
    </header>
  );
}
