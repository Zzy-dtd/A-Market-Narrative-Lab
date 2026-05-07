import json
import os

from src.api_settings import DEFAULT_MODEL, normalize_model_name


MOCK_NOTICE = "[Mock response - set OPENAI_API_KEY to enable live model output]"


class LLMClient:
    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        mock: bool = False,
        enable_web_search: bool = False,
    ):
        self.model = normalize_model_name(model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL))
        self.api_key = api_key
        self.mock = mock
        self.enable_web_search = enable_web_search

    def generate(self, instructions: str, user_input: str) -> str:
        if self.mock or not self.api_key:
            return self._mock_response(user_input)

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("The openai package is required for live model output.") from exc

        client = OpenAI(api_key=self.api_key)
        kwargs = {
            "model": self.model,
            "instructions": instructions,
            "input": user_input,
        }
        if self.enable_web_search:
            kwargs["tools"] = [{"type": "web_search"}]

        response = client.responses.create(**kwargs)
        return response.output_text

    def _mock_response(self, user_input: str) -> str:
        if "valid JSON only" in user_input or "learning_takeaway" in user_input:
            return json.dumps(
                {
                    "responses": [
                        {
                            "persona_id": "value_allocator",
                            "persona_name": "Long-Term Value Allocator",
                            "message": "A high-growth story can justify paying more, but it cannot make valuation disappear. This persona would ask what future expectations are already embedded in the price, and whether the current price leaves room for uncertainty, disappointment, or slower adoption.",
                        },
                        {
                            "persona_id": "market_structure_trader",
                            "persona_name": "Market Structure Trader",
                            "message": "The shorter-term question is whether investors are already crowded into the same narrative. If everyone is positioned for the same outcome, liquidity, options activity, and forced flows can matter as much as the fundamental story for a while.",
                        },
                        {
                            "persona_id": "behavioral_contrarian",
                            "persona_name": "Behavioral Contrarian",
                            "message": "This argument is powerful because it turns FOMO into something that feels rational. Investors may not only be buying growth; they may be buying a story that protects them from feeling left behind.",
                        },
                    ],
                    "learning_takeaway": "The lesson is that a growth narrative can be economically meaningful and psychologically dangerous at the same time. Different participants focus on different risks because they define the game differently.",
                },
                indent=2,
            )

        persona_line = "this persona"
        if "Long-Term Value Allocator" in user_input:
            persona_line = "a long-term value allocator"
        elif "Market Structure Trader" in user_input:
            persona_line = "a market structure trader"
        elif "Behavioral Contrarian" in user_input:
            persona_line = "a behavioral contrarian"

        return (
            f"{MOCK_NOTICE}\n\n"
            f"I would treat this as a question about how {persona_line} separates a market story from a reasoning framework. "
            "The first move is not to ask whether the crowd is right or wrong, but to ask what the crowd is assuming. "
            "Is recent price movement being used as evidence? Are investors changing the story because the price changed? "
            "Or is there new information that genuinely changes the long-term economics, positioning, or psychology around the asset?\n\n"
            "The useful habit is to slow the narrative down. Identify who believes it, what evidence would confirm it, what would weaken it, and what kind of risk this participant is most worried about. "
            "Learning takeaway: a market narrative is most educational when it shows you how different investors define risk, evidence, and time horizon."
        )
