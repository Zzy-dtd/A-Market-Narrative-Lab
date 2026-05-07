import html
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.demo_cases import DEMO_CASES
from src.llm_client import LLMClient
from src.persona_loader import load_all_personas
from src.prompt_builder import (
    build_roundtable_prompt,
    build_single_persona_prompt,
    persona_to_text,
)
from src.response_parser import parse_roundtable_json
from src.safety_filter import soften_recommendation_language


ROOT = Path(__file__).parent
PERSONA_DIR = ROOT / "personas"
PROMPT_DIR = ROOT / "prompts"
COMPACT_DISCLAIMER = "Educational analysis only. No buy/sell recommendations or price targets."

PERSONA_META = {
    "Long-Term Value Allocator": {
        "persona_id": "value_allocator",
        "initials": "LVA",
        "color": "#246b55",
        "greeting": "Ask me how a long-term capital allocator would frame this.",
    },
    "Market Structure Trader": {
        "persona_id": "market_structure_trader",
        "initials": "MST",
        "color": "#6d50a2",
        "greeting": "Ask me who may be forced to buy or sell.",
    },
    "Behavioral Contrarian": {
        "persona_id": "behavioral_contrarian",
        "initials": "BC",
        "color": "#ad5b34",
        "greeting": "Ask me what the crowd may be believing.",
    },
}

PERSONA_ID_TO_NAME = {
    meta["persona_id"]: name for name, meta in PERSONA_META.items()
}


def read_prompt(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8")


def escape_text(value: str) -> str:
    return html.escape(value).replace("\n", "<br>")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f2ea;
            color: #1f2937;
        }
        [data-testid="stSidebar"] {
            display: none;
        }
        .block-container {
            max-width: 1100px;
            padding-top: 1.6rem;
            padding-bottom: 6rem;
        }
        .lab-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: .8rem;
        }
        .lab-title {
            font-size: 2.05rem;
            line-height: 1.05;
            font-weight: 760;
            letter-spacing: 0;
            margin: 0;
        }
        .lab-subtitle {
            margin-top: .35rem;
            color: #596273;
            font-size: 1rem;
        }
        .compact-disclaimer {
            color: #6b7280;
            font-size: .82rem;
            margin-top: .35rem;
        }
        .scene {
            margin-top: 1rem;
            min-height: 520px;
            border: 1px solid rgba(71, 85, 105, .13);
            border-radius: 24px;
            background:
                radial-gradient(circle at 50% 18%, rgba(255,255,255,.9), rgba(255,255,255,.56) 36%, rgba(240,230,215,.55) 100%);
            box-shadow: 0 22px 70px rgba(66, 50, 30, .10);
            padding: 1.2rem;
            position: relative;
            overflow: hidden;
        }
        .user-question {
            max-width: 760px;
            margin: .4rem auto 1.1rem auto;
            padding: .85rem 1rem;
            border-radius: 18px;
            background: #1f2937;
            color: #fff;
            font-size: .95rem;
            line-height: 1.42;
            box-shadow: 0 12px 30px rgba(31, 41, 55, .16);
        }
        .avatar {
            width: 66px;
            height: 66px;
            border-radius: 999px;
            display: grid;
            place-items: center;
            color: white;
            font-weight: 760;
            font-size: .95rem;
            box-shadow: 0 12px 28px rgba(31, 41, 55, .16);
            margin: 0 auto .45rem;
        }
        .persona-label {
            text-align: center;
            font-weight: 720;
            color: #1f2937;
            font-size: .92rem;
            line-height: 1.25;
        }
        .speech-bubble {
            background: #fffdf9;
            border: 1px solid rgba(71, 85, 105, .13);
            border-radius: 18px;
            padding: 16px 20px;
            box-shadow: 0 14px 36px rgba(66, 50, 30, .10);
            line-height: 1.45;
            font-size: .95rem;
            color: #1f2937;
            max-width: 520px;
            position: relative;
        }
        .speech-bubble::after {
            content: "";
            position: absolute;
            left: 50%;
            bottom: -10px;
            width: 18px;
            height: 18px;
            background: #fffdf9;
            border-right: 1px solid rgba(71, 85, 105, .13);
            border-bottom: 1px solid rgba(71, 85, 105, .13);
            transform: translateX(-50%) rotate(45deg);
        }
        .one-scene {
            display: grid;
            grid-template-rows: 1fr auto;
            align-items: center;
            justify-items: center;
            min-height: 430px;
            gap: 1rem;
        }
        .one-bubble {
            align-self: end;
        }
        .one-avatar {
            align-self: start;
        }
        .roundtable-scene {
            display: grid;
            grid-template-columns: 1fr 210px 1fr;
            grid-template-rows: auto 1fr auto;
            gap: 1rem;
            min-height: 450px;
            align-items: center;
        }
        .seat-top {
            grid-column: 2;
            grid-row: 1;
            justify-self: center;
        }
        .seat-left {
            grid-column: 1;
            grid-row: 2;
            justify-self: end;
        }
        .seat-right {
            grid-column: 3;
            grid-row: 2;
            justify-self: start;
        }
        .round-seat {
            width: min(100%, 300px);
        }
        .round-seat .speech-bubble {
            min-height: 120px;
        }
        .table-wrap {
            grid-column: 2;
            grid-row: 2;
            justify-self: center;
            align-self: center;
        }
        .round-table {
            width: 210px;
            height: 118px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: linear-gradient(180deg, #dec9a8, #c8ad82);
            color: #5d472b;
            font-weight: 740;
            box-shadow: 0 18px 45px rgba(92, 68, 38, .20);
            border: 1px solid rgba(92, 68, 38, .12);
        }
        .takeaway {
            grid-column: 1 / -1;
            grid-row: 3;
            max-width: 780px;
            justify-self: center;
            background: rgba(255, 253, 249, .78);
            border: 1px solid rgba(71, 85, 105, .12);
            border-radius: 16px;
            padding: .85rem 1rem;
            color: #374151;
            line-height: 1.42;
            box-shadow: 0 10px 30px rgba(66, 50, 30, .07);
        }
        .takeaway-label {
            font-weight: 760;
            margin-bottom: .25rem;
            color: #1f2937;
        }
        .input-area {
            margin-top: 1rem;
            padding: .9rem;
            border-radius: 18px;
            background: rgba(255, 253, 249, .72);
            border: 1px solid rgba(71, 85, 105, .12);
        }
        .status-pill {
            display: inline-block;
            padding: .32rem .56rem;
            border-radius: 999px;
            border: 1px solid rgba(71, 85, 105, .16);
            background: #fffdf9;
            color: #4b5563;
            font-size: .82rem;
            margin: .15rem .25rem .15rem 0;
        }
        .history-user {
            color: #4b5563;
            margin-bottom: .25rem;
        }
        .history-persona {
            margin-bottom: .75rem;
        }
        @media (max-width: 850px) {
            .roundtable-scene {
                display: block;
            }
            .round-seat {
                width: 100%;
                margin: 1rem auto;
            }
            .table-wrap {
                display: flex;
                justify-content: center;
                margin: 1rem 0;
            }
            .speech-bubble {
                max-width: 100%;
            }
            .scene {
                padding: .9rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def persona_meta(persona_name: str) -> dict:
    return PERSONA_META[persona_name]


def persona_by_id(personas: dict[str, dict], persona_id: str) -> dict | None:
    name = PERSONA_ID_TO_NAME.get(persona_id)
    return personas.get(name) if name else None


def render_header() -> None:
    st.markdown(
        f"""
        <div class="lab-header">
            <div>
                <h1 class="lab-title">Market Narrative Lab</h1>
                <div class="lab-subtitle">Learn how different investors think, not copy their trades.</div>
                <div class="compact-disclaimer">{COMPACT_DISCLAIMER}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mode_selector() -> str:
    return st.radio(
        "Mode",
        ["One-on-One", "Roundtable"],
        horizontal=True,
        label_visibility="collapsed",
        key="mode",
    )


def render_persona_selector(personas: dict[str, dict]) -> str:
    return st.selectbox(
        "Choose a market participant",
        list(personas.keys()),
        key="selected_persona_name",
    )


def render_avatar(persona_id: str, persona_name: str, initials: str, color: str) -> str:
    return f"""
    <div class="avatar" style="background:{color};">{html.escape(initials)}</div>
    <div class="persona-label">{html.escape(persona_name)}</div>
    """


def render_speech_bubble(message: str, persona_id: str | None = None) -> str:
    class_name = f" speech-{persona_id}" if persona_id else ""
    return f"""<div class="speech-bubble{class_name}">{escape_text(message)}</div>"""


def render_user_question(question: str) -> str:
    if not question:
        return ""
    return f"""<div class="user-question">{escape_text(question)}</div>"""


def render_one_on_one_scene(selected_persona: dict, latest_message: str) -> None:
    name = selected_persona["name"]
    meta = persona_meta(name)
    message = latest_message or meta["greeting"]
    scene = f"""
    <div class="scene one-scene">
        {render_user_question(st.session_state.get("latest_question", ""))}
        <div class="one-bubble">{render_speech_bubble(message, meta["persona_id"])}</div>
        <div class="one-avatar">{render_avatar(meta["persona_id"], name, meta["initials"], meta["color"])}</div>
    </div>
    """
    st.markdown(scene, unsafe_allow_html=True)


def render_roundtable_seat(persona: dict, message: str) -> str:
    name = persona["name"]
    meta = persona_meta(name)
    return f"""
    <div class="round-seat">
        {render_speech_bubble(message or meta["greeting"], meta["persona_id"])}
        <div style="height:18px;"></div>
        {render_avatar(meta["persona_id"], name, meta["initials"], meta["color"])}
    </div>
    """


def render_roundtable_scene(
    personas: dict[str, dict],
    latest_messages_by_persona: dict[str, str],
    learning_takeaway: str,
) -> None:
    value = personas["Long-Term Value Allocator"]
    trader = personas["Market Structure Trader"]
    contrarian = personas["Behavioral Contrarian"]
    takeaway = learning_takeaway or "Ask a question and listen for how time horizon, incentives, and crowd psychology change the answer."
    scene = f"""
    <div class="scene">
        {render_user_question(st.session_state.get("latest_question", ""))}
        <div class="roundtable-scene">
            <div class="seat-top">{render_roundtable_seat(value, latest_messages_by_persona.get("value_allocator", ""))}</div>
            <div class="seat-left">{render_roundtable_seat(contrarian, latest_messages_by_persona.get("behavioral_contrarian", ""))}</div>
            <div class="table-wrap"><div class="round-table">Roundtable</div></div>
            <div class="seat-right">{render_roundtable_seat(trader, latest_messages_by_persona.get("market_structure_trader", ""))}</div>
            <div class="takeaway">
                <div class="takeaway-label">Learning Takeaway</div>
                {escape_text(takeaway)}
            </div>
        </div>
    </div>
    """
    st.markdown(scene, unsafe_allow_html=True)


def render_input_bar() -> bool:
    with st.container():
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        st.text_area(
            "Ask the lab",
            key="question_text",
            height=96,
            placeholder="Ask about a stock, market narrative, investor behavior, or market regime...",
        )
        send = st.button("Send", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    return send


def render_demo_questions() -> None:
    with st.expander("Demo questions", expanded=False):
        columns = st.columns(2)
        for index, case in enumerate(DEMO_CASES):
            with columns[index % 2]:
                if st.button(case["title"], key=f"demo_{index}", use_container_width=True):
                    st.session_state.question_text = case["text"]


def render_settings_expander(personas: dict[str, dict], has_api_key: bool) -> None:
    with st.expander("Settings / API status / persona details", expanded=False):
        st.text_input("Model name", key="model_name")
        st.checkbox(
            "Mock mode",
            key="mock_mode",
            help="Use deterministic demo output instead of calling the OpenAI API.",
        )
        current_output = "Live OpenAI call" if has_api_key and not st.session_state.mock_mode else "Mock output"
        st.markdown(
            f"""
            <span class="status-pill">OpenAI API: {'configured' if has_api_key else 'not configured'}</span>
            <span class="status-pill">Current output: {current_output}</span>
            <span class="status-pill">News API: not connected</span>
            """,
            unsafe_allow_html=True,
        )
        st.caption(COMPACT_DISCLAIMER)
        st.markdown("#### Persona cards")
        for persona in personas.values():
            st.markdown(f"**{persona['name']}**")
            st.caption(persona_to_text(persona))


def get_latest_messages_by_persona(session_state) -> dict[str, str]:
    messages = {}
    for message in session_state.get("messages", []):
        if message.get("role") == "persona" and message.get("persona_id"):
            messages[message["persona_id"]] = message.get("content", "")
    return messages


def render_history() -> None:
    with st.expander("Conversation history", expanded=False):
        if not st.session_state.messages:
            st.caption("No conversation yet.")
            return
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="history-user"><strong>You:</strong> {escape_text(message["content"])}</div>', unsafe_allow_html=True)
            elif message["role"] == "persona":
                st.markdown(
                    f'<div class="history-persona"><strong>{html.escape(message["persona_name"])}:</strong> {escape_text(message["content"])}</div>',
                    unsafe_allow_html=True,
                )
            elif message["role"] == "takeaway":
                st.markdown(f'<div class="history-persona"><strong>Learning Takeaway:</strong> {escape_text(message["content"])}</div>', unsafe_allow_html=True)


def init_session(personas: dict[str, dict]) -> None:
    st.session_state.setdefault("mode", "One-on-One")
    st.session_state.setdefault("selected_persona_name", list(personas.keys())[0])
    st.session_state.setdefault("model_name", os.getenv("OPENAI_MODEL", "gpt-5.2"))
    st.session_state.setdefault("mock_mode", not bool(os.getenv("OPENAI_API_KEY")))
    st.session_state.setdefault("question_text", "")
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("latest_question", "")
    st.session_state.setdefault("latest_one_on_one_message", "")
    st.session_state.setdefault("latest_learning_takeaway", "")
    st.session_state.setdefault("roundtable_parse_error", "")


def append_user_message(question: str, mode: str) -> None:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "mode": "one_on_one" if mode == "One-on-One" else "roundtable",
        }
    )


def handle_one_on_one_response(persona: dict, response: str) -> None:
    name = persona["name"]
    meta = persona_meta(name)
    content = soften_recommendation_language(response).strip()
    st.session_state.latest_one_on_one_message = content
    st.session_state.messages.append(
        {
            "role": "persona",
            "persona_id": meta["persona_id"],
            "persona_name": name,
            "content": content,
        }
    )


def handle_roundtable_response(raw_response: str) -> None:
    parsed = parse_roundtable_json(raw_response)
    st.session_state.roundtable_parse_error = parsed.get("parse_error", "")

    if parsed.get("parse_error"):
        fallback = soften_recommendation_language(parsed.get("raw_response", raw_response)).strip()
        st.session_state.messages.append(
            {
                "role": "persona",
                "persona_id": "moderator",
                "persona_name": "Moderator",
                "content": fallback,
            }
        )
        return

    for item in parsed["responses"]:
        content = soften_recommendation_language(item["message"]).strip()
        st.session_state.messages.append(
            {
                "role": "persona",
                "persona_id": item["persona_id"],
                "persona_name": item["persona_name"],
                "content": content,
            }
        )
    takeaway = soften_recommendation_language(parsed.get("learning_takeaway", "")).strip()
    st.session_state.latest_learning_takeaway = takeaway
    if takeaway:
        st.session_state.messages.append({"role": "takeaway", "content": takeaway})


def main() -> None:
    load_dotenv()
    st.set_page_config(page_title="Market Narrative Lab", page_icon="MNL", layout="wide")
    inject_css()

    try:
        personas = load_all_personas(str(PERSONA_DIR))
    except Exception as exc:
        st.error(f"Could not load personas: {exc}")
        st.stop()

    init_session(personas)
    render_header()
    render_mode_selector()
    if st.session_state.mode == "One-on-One":
        render_persona_selector(personas)

    latest_messages = get_latest_messages_by_persona(st.session_state)
    if st.session_state.mode == "One-on-One":
        selected_persona = personas[st.session_state.selected_persona_name]
        selected_id = persona_meta(selected_persona["name"])["persona_id"]
        latest = latest_messages.get(selected_id, st.session_state.latest_one_on_one_message)
        render_one_on_one_scene(selected_persona, latest)
    else:
        if st.session_state.roundtable_parse_error:
            st.warning("Roundtable response was not valid JSON, so the raw response was saved in history.")
        render_roundtable_scene(personas, latest_messages, st.session_state.latest_learning_takeaway)

    render_demo_questions()
    send = render_input_bar()
    render_settings_expander(personas, bool(os.getenv("OPENAI_API_KEY")))
    render_history()

    if send:
        question = st.session_state.question_text.strip()
        if not question:
            st.warning("Please enter a market question or narrative.")
            st.stop()

        base_prompt = read_prompt("base_system_prompt.txt")
        if st.session_state.mode == "One-on-One":
            persona = personas[st.session_state.selected_persona_name]
            instructions, user_input = build_single_persona_prompt(
                base_prompt,
                read_prompt("single_persona_prompt.txt"),
                persona,
                question,
            )
        else:
            instructions, user_input = build_roundtable_prompt(
                base_prompt,
                read_prompt("roundtable_prompt.txt"),
                list(personas.values()),
                question,
            )

        client = LLMClient(model=st.session_state.model_name, mock=st.session_state.mock_mode)
        with st.spinner("Thinking through the narrative..."):
            try:
                response = client.generate(instructions, user_input)
            except Exception as exc:
                st.error(f"Model call failed: {exc}")
                st.stop()

        st.session_state.latest_question = question
        append_user_message(question, st.session_state.mode)
        if st.session_state.mode == "One-on-One":
            handle_one_on_one_response(personas[st.session_state.selected_persona_name], response)
        else:
            handle_roundtable_response(response)
        st.rerun()


if __name__ == "__main__":
    main()
