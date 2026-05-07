import json
import re

VALID_PERSONA_IDS = {
    "value_allocator",
    "market_structure_trader",
    "behavioral_contrarian",
}


def parse_roundtable_json(raw_response: str) -> dict:
    """Parse roundtable JSON and return normalized persona messages."""
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        return {
            "responses": [],
            "learning_takeaway": "",
            "parse_error": f"Invalid JSON: {exc}",
            "raw_response": raw_response,
        }

    if not isinstance(data, dict):
        return {
            "responses": [],
            "learning_takeaway": "",
            "parse_error": "Roundtable response must be a JSON object.",
            "raw_response": raw_response,
        }

    raw_responses = data.get("responses", [])
    if not isinstance(raw_responses, list):
        return {
            "responses": [],
            "learning_takeaway": "",
            "parse_error": "Roundtable response field 'responses' must be a list.",
            "raw_response": raw_response,
        }

    normalized = []
    for item in raw_responses:
        if not isinstance(item, dict):
            continue
        persona_id = str(item.get("persona_id", "")).strip()
        persona_name = str(item.get("persona_name", "")).strip()
        message = str(item.get("message", "")).strip()
        if persona_id in VALID_PERSONA_IDS and persona_name and message:
            normalized.append(
                {
                    "persona_id": persona_id,
                    "persona_name": persona_name,
                    "message": message,
                }
            )

    if not normalized:
        return {
            "responses": [],
            "learning_takeaway": "",
            "parse_error": "No valid persona responses found.",
            "raw_response": raw_response,
        }

    return {
        "responses": normalized,
        "learning_takeaway": str(data.get("learning_takeaway", "")).strip(),
        "parse_error": "",
        "raw_response": raw_response,
    }


def split_roundtable_response(response: str, persona_names: list[str]) -> dict[str, str]:
    """Split a markdown roundtable response into persona sections."""
    sections: dict[str, str] = {}
    headings = persona_names + ["Final Learning Takeaway"]
    escaped = "|".join(re.escape(name) for name in headings)
    pattern = re.compile(rf"^##\s+({escaped})\s*$", flags=re.MULTILINE)
    matches = list(pattern.finditer(response))

    for index, match in enumerate(matches):
        title = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(response)
        content = response[start:end].strip()
        if content:
            sections[title] = content

    if not sections:
        sections["Final Learning Takeaway"] = response.strip()

    return sections
