import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";
import { normalizeModelName, type ChatRequest } from "@/lib/api";
import { buildRoundtablePrompt, buildSinglePersonaPrompt } from "@/lib/promptBuilder";
import { parseRoundtableJson } from "@/lib/responseParser";
import { softenRecommendationLanguage } from "@/lib/safety";

export const runtime = "nodejs";

function cleanQuestion(question: unknown) {
  return typeof question === "string" ? question.trim() : "";
}

export async function POST(request: NextRequest) {
  let body: ChatRequest;
  try {
    body = (await request.json()) as ChatRequest;
  } catch {
    return NextResponse.json({ error: "Invalid request body." }, { status: 400 });
  }

  const question = cleanQuestion(body.question);
  const apiKey = typeof body.apiKey === "string" ? body.apiKey.trim() : "";
  if (!apiKey) {
    return NextResponse.json(
      { error: "Enter your OpenAI API key in Settings to start chatting." },
      { status: 400 },
    );
  }
  if (!question) {
    return NextResponse.json({ error: "Ask a question before sending." }, { status: 400 });
  }

  const model = normalizeModelName(body.model || "");
  const prompt =
    body.mode === "roundtable"
      ? buildRoundtablePrompt(question)
      : buildSinglePersonaPrompt(body.personaId || "value_allocator", question);

  const client = new OpenAI({ apiKey });
  const kwargs: Record<string, unknown> = {
    model,
    instructions: prompt.instructions,
    input: prompt.userInput,
  };
  if (body.enableWebSearch) {
    kwargs.tools = [{ type: "web_search" }];
  }

  try {
    const response = await client.responses.create(kwargs as any);
    const output = response.output_text || "";

    if (body.mode === "roundtable") {
      const parsed = parseRoundtableJson(output);
      if (!parsed.ok) {
        return NextResponse.json({ error: parsed.error }, { status: 502 });
      }
      return NextResponse.json({
        mode: "roundtable",
        responses: parsed.data.responses.map((item) => ({
          ...item,
          message: softenRecommendationLanguage(item.message),
        })),
        learning_takeaway: softenRecommendationLanguage(parsed.data.learning_takeaway),
      });
    }

    return NextResponse.json({
      mode: "one_on_one",
      message: softenRecommendationLanguage(output),
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "OpenAI request failed.";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}
