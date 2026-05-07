import { describe, expect, it } from "vitest";
import { getPersonaById, personas } from "./personas";

describe("personas", () => {
  it("finds each persona by stable id", () => {
    for (const persona of personas) {
      expect(getPersonaById(persona.id)?.name).toBe(persona.name);
    }
  });
});
