import { describe, expect, it } from "vitest";
import { buildRoundtablePrompt, buildSinglePersonaPrompt } from "./promptBuilder";

describe("promptBuilder", () => {
  it("builds a single persona prompt with the question and persona", () => {
    const prompt = buildSinglePersonaPrompt(
      "value_allocator",
      "Why are investors excited about AI stocks?",
    );

    expect(prompt.instructions).toContain("educational market-thinking mentor");
    expect(prompt.userInput).toContain("Long-Term Value Allocator");
    expect(prompt.userInput).toContain("Why are investors excited about AI stocks?");
  });

  it("builds a roundtable prompt with all persona ids and question", () => {
    const prompt = buildRoundtablePrompt("Why does price movement change the story?");

    expect(prompt.userInput).toContain("value_allocator");
    expect(prompt.userInput).toContain("market_structure_trader");
    expect(prompt.userInput).toContain("behavioral_contrarian");
    expect(prompt.userInput).toContain("Why does price movement change the story?");
  });
});
