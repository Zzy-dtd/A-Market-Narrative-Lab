import { personas } from "@/lib/personas";
import type { PersonaId } from "@/lib/types";

export function PersonaSelector({
  selectedPersonaId,
  onChange,
}: {
  selectedPersonaId: PersonaId;
  onChange: (id: PersonaId) => void;
}) {
  return (
    <div className="mx-auto mt-4 flex max-w-4xl flex-wrap justify-center gap-2 px-4">
      {personas.map((persona) => (
        <button
          key={persona.id}
          type="button"
          onClick={() => onChange(persona.id)}
          className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
            selectedPersonaId === persona.id
              ? "border-transparent text-white shadow-sm"
              : "border-slate-900/10 bg-white/70 text-slate-600 hover:bg-white"
          }`}
          style={selectedPersonaId === persona.id ? { backgroundColor: persona.color } : undefined}
        >
          {persona.name}
        </button>
      ))}
    </div>
  );
}
