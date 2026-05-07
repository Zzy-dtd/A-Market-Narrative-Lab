import type { Mode } from "@/lib/types";

export function ModeSelector({ mode, onChange }: { mode: Mode; onChange: (mode: Mode) => void }) {
  return (
    <div className="mx-auto mt-6 flex w-fit rounded-full border border-slate-900/10 bg-white/70 p-1 shadow-sm">
      {[
        ["one_on_one", "One-on-One"],
        ["roundtable", "Roundtable"],
      ].map(([value, label]) => (
        <button
          key={value}
          type="button"
          onClick={() => onChange(value as Mode)}
          className={`rounded-full px-5 py-2 text-sm font-semibold transition ${
            mode === value
              ? "bg-lab-text text-white shadow-sm"
              : "text-slate-600 hover:bg-white"
          }`}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
