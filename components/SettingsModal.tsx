import { personas } from "@/lib/personas";

export function SettingsModal({
  isOpen,
  apiKey,
  model,
  enableWebSearch,
  onClose,
  onApiKeyChange,
  onModelChange,
  onWebSearchChange,
}: {
  isOpen: boolean;
  apiKey: string;
  model: string;
  enableWebSearch: boolean;
  onClose: () => void;
  onApiKeyChange: (value: string) => void;
  onModelChange: (value: string) => void;
  onWebSearchChange: (value: boolean) => void;
}) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/30 px-4 backdrop-blur-sm">
      <div className="max-h-[88vh] w-full max-w-2xl overflow-y-auto rounded-[28px] bg-white p-6 shadow-scene">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-lab-text">Settings</h2>
            <p className="mt-1 text-sm text-slate-500">
              API keys entered here stay in this browser session only.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full border border-slate-900/10 px-3 py-1 text-sm font-semibold text-slate-600 hover:bg-slate-50"
          >
            Close
          </button>
        </div>

        <div className="mt-6 space-y-5">
          <label className="block">
            <span className="text-sm font-semibold text-lab-text">OpenAI API key</span>
            <input
              type="password"
              value={apiKey}
              onChange={(event) => onApiKeyChange(event.target.value)}
              placeholder="sk-..."
              className="mt-2 w-full rounded-2xl border border-slate-900/10 px-4 py-3 text-sm outline-none focus:border-slate-400"
            />
          </label>
          <label className="block">
            <span className="text-sm font-semibold text-lab-text">Model name</span>
            <input
              value={model}
              onChange={(event) => onModelChange(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-900/10 px-4 py-3 text-sm outline-none focus:border-slate-400"
            />
          </label>
          <label className="flex items-center gap-3 rounded-2xl border border-slate-900/10 px-4 py-3 text-sm text-slate-700">
            <input
              type="checkbox"
              checked={enableWebSearch}
              onChange={(event) => onWebSearchChange(event.target.checked)}
            />
            Enable web search
          </label>
          <p className="text-sm leading-relaxed text-slate-500">
            Without web search, the model only uses the prompt, persona cards, user input,
            and its internal knowledge. For current market narratives or recent events,
            enable web search or connect separate data APIs.
          </p>

          <div className="flex flex-wrap gap-2">
            <span className="rounded-full border border-slate-900/10 px-3 py-1 text-xs font-semibold text-slate-600">
              {apiKey ? "API key ready" : "API key missing"}
            </span>
            <span className="rounded-full border border-slate-900/10 px-3 py-1 text-xs font-semibold text-slate-600">
              {enableWebSearch ? "Web search enabled" : "Web search disabled"}
            </span>
            <span className="rounded-full border border-slate-900/10 px-3 py-1 text-xs font-semibold text-slate-600">
              Market data APIs: not connected
            </span>
          </div>

          <details className="rounded-2xl border border-slate-900/10 p-4">
            <summary className="cursor-pointer text-sm font-bold text-lab-text">
              Persona details
            </summary>
            <div className="mt-4 space-y-4">
              {personas.map((persona) => (
                <div key={persona.id}>
                  <div className="font-semibold text-lab-text">{persona.name}</div>
                  <p className="mt-1 text-sm leading-relaxed text-slate-500">
                    {persona.shortDescription}
                  </p>
                </div>
              ))}
            </div>
          </details>
        </div>
      </div>
    </div>
  );
}
