import os


MOCK_MODE = "Mock mode"
LIVE_MODE = "Live OpenAI API mode"


def resolve_openai_api_key(session_key: str | None = None) -> str:
    """Resolve API key from session input first, then environment fallback."""
    if session_key and session_key.strip():
        return session_key.strip()
    return os.getenv("OPENAI_API_KEY", "").strip()


def is_mock_mode(api_mode: str) -> bool:
    return api_mode == MOCK_MODE
