import type { Mode, PersonaId, RoundtableResponse } from "./types";

export type ChatRequest = {
  mode: Mode;
  question: string;
  personaId?: PersonaId;
  apiKey: string;
  model: string;
  enableWebSearch: boolean;
};

export type OneOnOneApiResponse = {
  mode: "one_on_one";
  message: string;
};

export type RoundtableApiResponse = RoundtableResponse & {
  mode: "roundtable";
};

export type ChatApiResponse = OneOnOneApiResponse | RoundtableApiResponse;

export function normalizeModelName(model: string) {
  const fallback = process.env.NEXT_PUBLIC_DEFAULT_MODEL || "gpt-5.2";
  const trimmed = model.trim();
  if (!trimmed) {
    return fallback;
  }
  return trimmed.toLowerCase().split(/\s+/).join("-");
}

export function friendlyApiError(error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  if (message.includes("model_not_found") || message.includes("does not exist")) {
    return "The selected model was not found or your account does not have access to it. Check the model name in Settings.";
  }
  if (message.includes("invalid_api_key") || message.includes("Incorrect API key")) {
    return "The OpenAI API key is invalid. Re-enter it in Settings.";
  }
  return "The OpenAI request failed. Check your API key, model name, and connection.";
}
