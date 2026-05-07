import json

from src.llm_client import LLMClient
from src.response_parser import parse_roundtable_json, split_roundtable_response
from src.safety_filter import DISCLAIMER, add_disclaimer


PERSONA_NAMES = [
    "Long-Term Value Allocator",
    "Market Structure Trader",
    "Behavioral Contrarian",
]


def test_split_roundtable_response_finds_persona_sections():
    response = """# Roundtable Discussion

## Long-Term Value Allocator
Value view.

## Market Structure Trader
Flow view.

## Behavioral Contrarian
Psychology view.

## Final Learning Takeaway
Learn from the disagreement.
"""

    sections = split_roundtable_response(response, PERSONA_NAMES)

    assert sections["Long-Term Value Allocator"] == "Value view."
    assert sections["Market Structure Trader"] == "Flow view."
    assert sections["Behavioral Contrarian"] == "Psychology view."
    assert sections["Final Learning Takeaway"] == "Learn from the disagreement."


def test_parse_roundtable_json_finds_persona_messages():
    raw = json.dumps(
        {
            "responses": [
                {
                    "persona_id": "value_allocator",
                    "persona_name": "Long-Term Value Allocator",
                    "message": "Value view.",
                },
                {
                    "persona_id": "market_structure_trader",
                    "persona_name": "Market Structure Trader",
                    "message": "Flow view.",
                },
                {
                    "persona_id": "behavioral_contrarian",
                    "persona_name": "Behavioral Contrarian",
                    "message": "Psychology view.",
                },
            ],
            "learning_takeaway": "Learn from the disagreement.",
        }
    )

    parsed = parse_roundtable_json(raw)

    assert parsed["parse_error"] == ""
    assert len(parsed["responses"]) == 3
    assert parsed["responses"][0]["persona_id"] == "value_allocator"
    assert parsed["learning_takeaway"] == "Learn from the disagreement."


def test_parse_roundtable_json_handles_invalid_json():
    parsed = parse_roundtable_json("not json")

    assert parsed["responses"] == []
    assert parsed["parse_error"]
    assert parsed["raw_response"] == "not json"


def test_mock_roundtable_response_is_valid_json_with_all_persona_ids():
    response = LLMClient(mock=True).generate(
        "instructions",
        "Return valid JSON only with responses and learning_takeaway.",
    )
    parsed = parse_roundtable_json(response)

    ids = {item["persona_id"] for item in parsed["responses"]}

    assert parsed["parse_error"] == ""
    assert ids == {"value_allocator", "market_structure_trader", "behavioral_contrarian"}


def test_llm_client_initializes_live_settings():
    client = LLMClient(
        model="test-model",
        api_key="session-key",
        mock=False,
        enable_web_search=True,
    )

    assert client.model == "test-model"
    assert client.api_key == "session-key"
    assert client.mock is False
    assert client.enable_web_search is True


def test_add_disclaimer_appends_disclaimer():
    response = add_disclaimer("Educational response.")

    assert DISCLAIMER in response
