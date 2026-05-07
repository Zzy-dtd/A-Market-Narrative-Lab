import { personas, requirePersonaById } from "@/lib/personas";
import type { PersonaId } from "@/lib/types";
import { PersonaAvatar } from "./PersonaAvatar";
import { SpeechBubble } from "./SpeechBubble";

type MessagesByPersona = Partial<Record<PersonaId, string>>;

export function OneOnOneScene({
  selectedPersonaId,
  latestQuestion,
  message,
}: {
  selectedPersonaId: PersonaId;
  latestQuestion: string;
  message?: string;
}) {
  const persona = requirePersonaById(selectedPersonaId);
  return (
    <section className="mx-auto mt-6 min-h-[520px] w-full max-w-6xl rounded-[32px] border border-slate-900/10 bg-white/45 px-5 py-7 shadow-scene sm:px-8">
      {latestQuestion ? (
        <div className="mx-auto mb-8 max-w-3xl rounded-[22px] bg-lab-text px-5 py-4 text-sm leading-relaxed text-white shadow-bubble">
          {latestQuestion}
        </div>
      ) : null}
      <div className="flex min-h-[390px] flex-col items-center justify-center gap-9">
        <SpeechBubble className="text-center">{message || persona.greeting}</SpeechBubble>
        <PersonaAvatar persona={persona} size="lg" />
      </div>
    </section>
  );
}

function RoundtableSeat({ personaId, message }: { personaId: PersonaId; message?: string }) {
  const persona = requirePersonaById(personaId);
  return (
    <div className="flex w-full max-w-[310px] flex-col items-center gap-5">
      <SpeechBubble>{message || persona.greeting}</SpeechBubble>
      <PersonaAvatar persona={persona} />
    </div>
  );
}

export function RoundtableScene({
  latestQuestion,
  messagesByPersona,
  learningTakeaway,
}: {
  latestQuestion: string;
  messagesByPersona: MessagesByPersona;
  learningTakeaway?: string;
}) {
  return (
    <section className="mx-auto mt-6 min-h-[620px] w-full max-w-6xl rounded-[32px] border border-slate-900/10 bg-white/45 px-5 py-7 shadow-scene sm:px-8">
      {latestQuestion ? (
        <div className="mx-auto mb-8 max-w-3xl rounded-[22px] bg-lab-text px-5 py-4 text-sm leading-relaxed text-white shadow-bubble">
          {latestQuestion}
        </div>
      ) : null}
      <div className="grid min-h-[470px] grid-cols-1 items-center gap-6 lg:grid-cols-[1fr_230px_1fr] lg:grid-rows-[auto_1fr_auto]">
        <div className="justify-self-center lg:col-start-2 lg:row-start-1">
          <RoundtableSeat
            personaId="value_allocator"
            message={messagesByPersona.value_allocator}
          />
        </div>
        <div className="justify-self-center lg:col-start-1 lg:row-start-2 lg:justify-self-end">
          <RoundtableSeat
            personaId="behavioral_contrarian"
            message={messagesByPersona.behavioral_contrarian}
          />
        </div>
        <div className="flex justify-center lg:col-start-2 lg:row-start-2">
          <div className="grid h-32 w-56 place-items-center rounded-[50%] border border-amber-900/10 bg-lab-table font-bold text-amber-950 shadow-bubble">
            Roundtable
          </div>
        </div>
        <div className="justify-self-center lg:col-start-3 lg:row-start-2 lg:justify-self-start">
          <RoundtableSeat
            personaId="market_structure_trader"
            message={messagesByPersona.market_structure_trader}
          />
        </div>
        <div className="rounded-2xl border border-slate-900/10 bg-white/80 px-5 py-4 text-sm leading-relaxed text-slate-700 shadow-sm lg:col-span-3 lg:row-start-3 lg:mx-auto lg:max-w-3xl">
          <div className="mb-1 font-bold text-lab-text">Learning Takeaway</div>
          {learningTakeaway ||
            "Ask a question and listen for how time horizon, incentives, and crowd psychology change the answer."}
        </div>
      </div>
    </section>
  );
}

export function emptyMessagesByPersona(): MessagesByPersona {
  return Object.fromEntries(personas.map((persona) => [persona.id, ""])) as MessagesByPersona;
}
