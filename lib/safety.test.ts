import { describe, expect, it } from "vitest";
import { detectDirectRecommendation, softenRecommendationLanguage } from "./safety";

describe("safety", () => {
  it("detects obvious recommendation language", () => {
    expect(detectDirectRecommendation("You should buy this stock.")).toBe(true);
  });

  it("adds an educational warning", () => {
    expect(softenRecommendationLanguage("This is a strong buy.")).toContain(
      "educational analysis only",
    );
  });
});
