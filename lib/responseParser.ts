import type { RoundtablePersonaResponse, RoundtableResponse } from "./types";

const validPersonaIds = new Set([
  "value_allocator",
  "market_structure_trader",
  "behavioral_contrarian",
]);

export type ParsedRoundtable =
  | {
      ok: true;
      data: RoundtableResponse;
    }
  | {
      ok: false;
      error: string;
    };

function isPersonaResponse(value: unknown): value is RoundtablePersonaResponse {
  if (!value || typeof value !== "object") {
    return false;
  }
  const item = value as Record<string, unknown>;
  return (
    typeof item.persona_id === "string" &&
    validPersonaIds.has(item.persona_id) &&
    typeof item.persona_name === "string" &&
    typeof item.message === "string" &&
    item.message.trim().length > 0
  );
}

export function parseRoundtableJson(raw: string): ParsedRoundtable {
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (!parsed || typeof parsed !== "object") {
      return { ok: false, error: "Roundtable response was not a JSON object." };
    }
    const record = parsed as Record<string, unknown>;
    if (!Array.isArray(record.responses)) {
      return { ok: false, error: "Roundtable response did not include a responses array." };
    }
    const responses = record.responses.filter(isPersonaResponse);
    if (responses.length === 0) {
      return { ok: false, error: "Roundtable response did not include valid persona messages." };
    }
    return {
      ok: true,
      data: {
        responses,
        learning_takeaway:
          typeof record.learning_takeaway === "string" ? record.learning_takeaway : "",
      },
    };
  } catch {
    return { ok: false, error: "Roundtable response was not valid JSON." };
  }
}
