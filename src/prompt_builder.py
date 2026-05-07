def _format_value(value: object, indent: str = "") -> str:
    if isinstance(value, list):
        return "\n".join(f"{indent}- {item}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"{indent}{key}: {_format_value(val, indent + '  ')}" for key, val in value.items())
    return str(value)


def persona_to_text(persona: dict) -> str:
    """Convert a persona dictionary into a readable prompt card."""
    sections = []
    for key, value in persona.items():
        title = key.replace("_", " ").title()
        sections.append(f"{title}:\n{_format_value(value)}")
    return "\n\n".join(sections)


def build_single_persona_prompt(
    base_prompt: str,
    single_template: str,
    persona: dict,
    user_question: str,
) -> tuple[str, str]:
    """Build instructions and user input for a single-persona response."""
    persona_card = persona_to_text(persona)
    user_input = single_template.format(
        persona_card=persona_card,
        user_question=user_question,
    )
    return base_prompt.strip(), user_input.strip()


def build_roundtable_prompt(
    base_prompt: str,
    roundtable_template: str,
    personas: list[dict],
    user_question: str,
) -> tuple[str, str]:
    """Build instructions and user input for a multi-persona roundtable."""
    persona_cards = "\n\n---\n\n".join(persona_to_text(persona) for persona in personas)
    user_input = roundtable_template.format(
        persona_cards=persona_cards,
        user_question=user_question,
    )
    return base_prompt.strip(), user_input.strip()
