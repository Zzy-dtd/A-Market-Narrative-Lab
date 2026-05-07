"use client";

import { useEffect, useMemo, useState } from "react";
import { Header } from "@/components/Header";
import { ModeSelector } from "@/components/ModeSelector";
import { PersonaSelector } from "@/components/PersonaSelector";
import { OneOnOneScene, RoundtableScene, emptyMessagesByPersona } from "@/components/ConversationScenes";
import { InputBar } from "@/components/InputBar";
import { SettingsModal } from "@/components/SettingsModal";
import { HistoryPanel } from "@/components/HistoryPanel";
import { friendlyApiError, type ChatApiResponse } from "@/lib/api";
import { requirePersonaById } from "@/lib/personas";
import type { ConversationEntry, Mode, PersonaId } from "@/lib/types";

const defaultModel = process.env.NEXT_PUBLIC_DEFAULT_MODEL || "gpt-5.2";

export default function Home() {
  const [mode, setMode] = useState<Mode>("one_on_one");
  const [selectedPersonaId, setSelectedPersonaId] = useState<PersonaId>("value_allocator");
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState(defaultModel);
  const [enableWebSearch, setEnableWebSearch] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const [latestQuestion, setLatestQuestion] = useState("");
  const [oneOnOneMessage, setOneOnOneMessage] = useState("");
  const [roundtableMessages, setRoundtableMessages] = useState(emptyMessagesByPersona());
  const [learningTakeaway, setLearningTakeaway] = useState("");
  const [history, setHistory] = useState<ConversationEntry[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const selectedPersona = useMemo(
    () => requirePersonaById(selectedPersonaId),
    [selectedPersonaId],
  );

  useEffect(() => {
    const storedKey = window.sessionStorage.getItem("market_narrative_lab_api_key");
    const storedModel = window.sessionStorage.getItem("market_narrative_lab_model");
    const storedWebSearch = window.sessionStorage.getItem("market_narrative_lab_web_search");
    if (storedKey) {
      setApiKey(storedKey);
    }
    if (storedModel) {
      setModel(storedModel);
    }
    if (storedWebSearch) {
      setEnableWebSearch(storedWebSearch === "true");
    }
  }, []);

  function handleApiKeyChange(value: string) {
    setApiKey(value);
    if (value) {
      window.sessionStorage.setItem("market_narrative_lab_api_key", value);
    } else {
      window.sessionStorage.removeItem("market_narrative_lab_api_key");
    }
  }

  function handleModelChange(value: string) {
    setModel(value);
    window.sessionStorage.setItem("market_narrative_lab_model", value);
  }

  function handleWebSearchChange(value: boolean) {
    setEnableWebSearch(value);
    window.sessionStorage.setItem("market_narrative_lab_web_search", String(value));
  }

  async function sendQuestion() {
    const trimmedQuestion = question.trim();
    setError("");
    if (!trimmedQuestion) {
      setError("Ask a question before sending.");
      return;
    }
    if (!apiKey.trim()) {
      setError("Enter your OpenAI API key in Settings to start chatting.");
      setSettingsOpen(true);
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mode,
          question: trimmedQuestion,
          personaId: selectedPersonaId,
          apiKey,
          model,
          enableWebSearch,
        }),
      });

      const data = (await response.json()) as ChatApiResponse | { error?: string };
      if (!response.ok || "error" in data) {
        throw new Error("error" in data && data.error ? data.error : "Request failed.");
      }

      setLatestQuestion(trimmedQuestion);
      setHistory((current) => [
        ...current,
        { role: "user", mode, content: trimmedQuestion },
      ]);

      if (data.mode === "one_on_one") {
        setOneOnOneMessage(data.message);
        setHistory((current) => [
          ...current,
          {
            role: "persona",
            personaId: selectedPersona.id,
            personaName: selectedPersona.name,
            content: data.message,
          },
        ]);
      } else {
        const nextMessages = emptyMessagesByPersona();
        for (const item of data.responses) {
          nextMessages[item.persona_id] = item.message;
        }
        setRoundtableMessages(nextMessages);
        setLearningTakeaway(data.learning_takeaway);
        setHistory((current) => [
          ...current,
          ...data.responses.map((item) => ({
            role: "persona" as const,
            personaId: item.persona_id,
            personaName: item.persona_name,
            content: item.message,
          })),
          { role: "takeaway", content: data.learning_takeaway },
        ]);
      }
      setQuestion("");
    } catch (caught) {
      setError(friendlyApiError(caught));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen pb-36">
      <Header onOpenSettings={() => setSettingsOpen(true)} />
      <div className="mx-auto mt-4 flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 sm:px-6">
        <ModeSelector mode={mode} onChange={setMode} />
        <div className="flex flex-wrap gap-2 text-xs font-semibold text-slate-600">
          <span className="rounded-full border border-slate-900/10 bg-white/70 px-3 py-1">
            {apiKey ? "API key ready" : "API key missing"}
          </span>
          <span className="rounded-full border border-slate-900/10 bg-white/70 px-3 py-1">
            {enableWebSearch ? "Web search enabled" : "Web search disabled"}
          </span>
        </div>
      </div>

      {mode === "one_on_one" ? (
        <>
          <PersonaSelector
            selectedPersonaId={selectedPersonaId}
            onChange={setSelectedPersonaId}
          />
          <OneOnOneScene
            selectedPersonaId={selectedPersonaId}
            latestQuestion={latestQuestion}
            message={oneOnOneMessage}
          />
        </>
      ) : (
        <RoundtableScene
          latestQuestion={latestQuestion}
          messagesByPersona={roundtableMessages}
          learningTakeaway={learningTakeaway}
        />
      )}

      {error ? (
        <div className="mx-auto mt-5 max-w-4xl rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm font-semibold text-red-800">
          {error}
        </div>
      ) : null}

      <HistoryPanel history={history} />

      <SettingsModal
        isOpen={settingsOpen}
        apiKey={apiKey}
        model={model}
        enableWebSearch={enableWebSearch}
        onClose={() => setSettingsOpen(false)}
        onApiKeyChange={handleApiKeyChange}
        onModelChange={handleModelChange}
        onWebSearchChange={handleWebSearchChange}
      />

      <InputBar
        question={question}
        isLoading={isLoading}
        onQuestionChange={setQuestion}
        onSend={sendQuestion}
      />
    </main>
  );
}
