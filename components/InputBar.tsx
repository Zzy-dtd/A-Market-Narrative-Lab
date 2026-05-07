export function InputBar({
  question,
  isLoading,
  onQuestionChange,
  onSend,
}: {
  question: string;
  isLoading: boolean;
  onQuestionChange: (value: string) => void;
  onSend: () => void;
}) {
  return (
    <div className="fixed inset-x-0 bottom-0 z-30 border-t border-slate-900/10 bg-[#F7F2EA]/90 px-4 py-4 backdrop-blur">
      <div className="mx-auto flex max-w-5xl gap-3 rounded-[28px] border border-slate-900/10 bg-white p-2 shadow-bubble">
        <textarea
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          onKeyDown={(event) => {
            if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
              onSend();
            }
          }}
          placeholder="Ask about a stock, market narrative, investor behavior, or market regime..."
          className="min-h-14 flex-1 resize-none rounded-[22px] px-4 py-3 text-sm leading-relaxed outline-none"
        />
        <button
          type="button"
          onClick={onSend}
          disabled={isLoading}
          className="rounded-[22px] bg-lab-text px-6 py-3 text-sm font-bold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? "Thinking" : "Send"}
        </button>
      </div>
    </div>
  );
}
