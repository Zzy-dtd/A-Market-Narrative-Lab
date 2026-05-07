import type { ReactNode } from "react";

export function SpeechBubble({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`speech-tail relative max-w-xl rounded-[22px] border border-slate-900/10 bg-white px-5 py-4 text-[15px] leading-relaxed text-lab-text shadow-bubble ${className}`}
    >
      {children}
    </div>
  );
}
