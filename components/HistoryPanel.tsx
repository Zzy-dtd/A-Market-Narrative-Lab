import type { ConversationEntry } from "@/lib/types";

export function HistoryPanel({ history }: { history: ConversationEntry[] }) {
  return (
    <details className="mx-auto mt-5 max-w-6xl rounded-2xl border border-slate-900/10 bg-white/60 px-5 py-4 text-sm">
      <summary className="cursor-pointer font-bold text-lab-text">Conversation history</summary>
      <div className="mt-4 space-y-3">
        {history.length === 0 ? (
          <p className="text-slate-500">No conversation yet.</p>
        ) : (
          history.map((entry, index) => {
            if (entry.role === "user") {
              return (
                <p key={index} className="text-slate-600">
                  <span className="font-bold text-lab-text">You:</span> {entry.content}
                </p>
              );
            }
            if (entry.role === "takeaway") {
              return (
                <p key={index} className="text-slate-600">
                  <span className="font-bold text-lab-text">Learning Takeaway:</span>{" "}
                  {entry.content}
                </p>
              );
            }
            return (
              <p key={index} className="text-slate-600">
                <span className="font-bold text-lab-text">{entry.personaName}:</span>{" "}
                {entry.content}
              </p>
            );
          })
        )}
      </div>
    </details>
  );
}
