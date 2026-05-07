from src.prompt_builder import (
    build_roundtable_prompt,
    build_single_persona_prompt,
    persona_to_text,
)


def test_build_roundtable_prompt_with_json_template_does_not_raise():
    personas = [
        {"name": "Long-Term Value Allocator"},
        {"name": "Market Structure Trader"},
        {"name": "Behavioral Contrarian"},
    ]
    with open("prompts/roundtable_prompt.txt", "r", encoding="utf-8") as file:
        template = file.read()

    _, user_input = build_roundtable_prompt(
        "Base instructions",
        template,
        personas,
        "Why are people saying Buffett missed the rally?",
    )

    assert '"responses"' in user_input
    assert "{persona_cards}" not in user_input
    assert "{user_question}" not in user_input


def test_persona_to_text_contains_persona_name():
    persona = {"name": "Long-Term Value Allocator", "core_beliefs": ["Price and value differ."]}

    text = persona_to_text(persona)

    assert isinstance(text, str)
    assert "Long-Term Value Allocator" in text


def test_build_single_persona_prompt_includes_user_question():
    persona = {"name": "Market Structure Trader"}
    question = "Why does a short squeeze narrative matter?"
    template = "Persona:\n{persona_card}\n\nQuestion:\n{user_question}"

    instructions, user_input = build_single_persona_prompt(
        "Base instructions",
        template,
        persona,
        question,
    )

    assert instructions == "Base instructions"
    assert question in user_input


def test_build_roundtable_prompt_includes_all_persona_names():
    personas = [
        {"name": "Long-Term Value Allocator"},
        {"name": "Market Structure Trader"},
        {"name": "Behavioral Contrarian"},
    ]
    template = "Personas:\n{persona_cards}\n\nQuestion:\n{user_question}"

    _, user_input = build_roundtable_prompt(
        "Base instructions",
        template,
        personas,
        "Why does price movement change the story?",
    )

    for persona in personas:
        assert persona["name"] in user_input
