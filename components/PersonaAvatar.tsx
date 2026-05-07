import type { Persona } from "@/lib/types";

export function PersonaAvatar({ persona, size = "md" }: { persona: Persona; size?: "md" | "lg" }) {
  const avatarSize = size === "lg" ? "h-24 w-24 text-lg" : "h-16 w-16 text-sm";
  return (
    <div className="flex flex-col items-center gap-3 text-center">
      <div
        className={`${avatarSize} grid place-items-center rounded-full font-bold text-white shadow-bubble`}
        style={{ backgroundColor: persona.color }}
      >
        {persona.initials}
      </div>
      <div className="max-w-[180px] text-sm font-semibold leading-tight text-lab-text">
        {persona.name}
      </div>
    </div>
  );
}
