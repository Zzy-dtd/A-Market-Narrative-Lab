export type PersonaId =
  | "value_allocator"
  | "market_structure_trader"
  | "behavioral_contrarian";

export type Mode = "one_on_one" | "roundtable";

export type Persona = {
  id: PersonaId;
  name: string;
  initials: string;
  color: string;
  greeting: string;
  shortDescription: string;
  coreBeliefs: string[];
  timeHorizon: string[];
  riskDefinition: string[];
  preferredEvidence: string[];
  speakingStyle: string[];
  restrictions: string[];
};

export type RoundtablePersonaResponse = {
  persona_id: PersonaId;
  persona_name: string;
  message: string;
};

export type RoundtableResponse = {
  responses: RoundtablePersonaResponse[];
  learning_takeaway: string;
};

export type ConversationEntry =
  | {
      role: "user";
      mode: Mode;
      content: string;
    }
  | {
      role: "persona";
      personaId: PersonaId;
      personaName: string;
      content: string;
    }
  | {
      role: "takeaway";
      content: string;
    };
