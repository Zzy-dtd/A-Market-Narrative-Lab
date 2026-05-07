import { describe, expect, it } from "vitest";
import { parseRoundtableJson } from "./responseParser";

describe("parseRoundtableJson", () => {
  it("parses valid roundtable JSON", () => {
    const parsed = parseRoundtableJson(
      JSON.stringify({
        responses: [
          {
            persona_id: "value_allocator",
            persona_name: "Long-Term Value Allocator",
            message: "Value view.",
          },
        ],
        learning_takeaway: "Compare frameworks.",
      }),
    );

    expect(parsed.ok).toBe(true);
    if (parsed.ok) {
      expect(parsed.data.responses[0].persona_id).toBe("value_allocator");
      expect(parsed.data.learning_takeaway).toBe("Compare frameworks.");
    }
  });

  it("rejects invalid JSON gracefully", () => {
    const parsed = parseRoundtableJson("not json");

    expect(parsed.ok).toBe(false);
  });
});
